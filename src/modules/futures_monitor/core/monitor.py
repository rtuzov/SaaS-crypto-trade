import asyncio
from typing import Dict, Optional, List
from datetime import datetime
from decimal import Decimal
import logging
from ..models.schemas import Position, PositionUpdate, UserPositions, MonitorSettings
from trade_executor.utils.binance import BinanceFuturesClient
import asyncpg
import os

logger = logging.getLogger(__name__)

class FuturesMonitor:
    def __init__(self):
        self.active_monitors: Dict[str, asyncio.Task] = {}
        self.settings: Dict[str, MonitorSettings] = {}
        self.positions: Dict[str, UserPositions] = {}
        
    async def get_db_connection(self):
        return await asyncpg.connect(
            host=os.getenv('POSTGRES_HOST', 'postgres'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
            database=os.getenv('POSTGRES_DB', 'trading')
        )
        
    async def get_user_api_keys(self, user_id: str) -> tuple[str, str]:
        conn = await self.get_db_connection()
        try:
            row = await conn.fetchrow(
                """
                SELECT api_key_enc 
                FROM core.user_api_keys 
                WHERE user_id = $1 AND exchange = 'binance'
                """,
                user_id
            )
            if not row:
                raise ValueError("API keys not found")
                
            # TODO: Decrypt api_key_enc using PGP_MASTER_KEY
            # For now, return dummy values
            return "dummy_key", "dummy_secret"
        finally:
            await conn.close()
            
    async def fetch_positions(self, user_id: str) -> List[Position]:
        try:
            api_key, api_secret = await self.get_user_api_keys(user_id)
            client = BinanceFuturesClient(api_key, api_secret)
            
            # Get positions from Binance
            positions = await client.get_positions()
            
            # Convert to our format
            return [
                Position(
                    symbol=pos['symbol'],
                    side=pos['side'],
                    entry_price=Decimal(str(pos['entryPrice'])),
                    current_price=Decimal(str(pos['markPrice'])),
                    size=Decimal(str(pos['positionAmt'])),
                    leverage=int(pos['leverage']),
                    pnl=Decimal(str(pos['unrealizedProfit'])),
                    pnl_percentage=Decimal(str(pos['unrealizedProfit'])) / Decimal(str(pos['positionAmt'])) * 100,
                    liquidation_price=Decimal(str(pos['liquidationPrice'])),
                    timestamp=datetime.fromtimestamp(pos['updateTime'] / 1000)
                )
                for pos in positions
                if Decimal(str(pos['positionAmt'])) != 0
            ]
        except Exception as e:
            logger.error(f"Error fetching positions for user {user_id}: {e}")
            return []
            
    async def monitor_user(self, user_id: str):
        settings = self.settings.get(user_id)
        if not settings or not settings.enabled:
            return
            
        while True:
            try:
                positions = await self.fetch_positions(user_id)
                
                if positions:
                    total_pnl = sum(p.pnl for p in positions)
                    total_size = sum(abs(p.size) for p in positions)
                    total_pnl_percentage = (total_pnl / total_size * 100) if total_size else Decimal('0')
                    
                    self.positions[user_id] = UserPositions(
                        user_id=user_id,
                        positions=positions,
                        total_pnl=total_pnl,
                        total_pnl_percentage=total_pnl_percentage,
                        last_update=datetime.now()
                    )
                    
                    # Check for alerts
                    if abs(total_pnl_percentage) >= settings.alert_threshold * 100:
                        # TODO: Send alert
                        pass
                        
            except Exception as e:
                logger.error(f"Error monitoring user {user_id}: {e}")
                
            await asyncio.sleep(settings.update_interval)
            
    async def start_monitoring(self, user_id: str, settings: MonitorSettings):
        self.settings[user_id] = settings
        
        if user_id in self.active_monitors:
            self.active_monitors[user_id].cancel()
            
        self.active_monitors[user_id] = asyncio.create_task(
            self.monitor_user(user_id)
        )
        
    async def stop_monitoring(self, user_id: str):
        if user_id in self.active_monitors:
            self.active_monitors[user_id].cancel()
            del self.active_monitors[user_id]
            
        if user_id in self.settings:
            del self.settings[user_id]
            
        if user_id in self.positions:
            del self.positions[user_id]
            
    def get_user_positions(self, user_id: str) -> Optional[UserPositions]:
        return self.positions.get(user_id)
        
    def get_all_positions(self) -> Dict[str, UserPositions]:
        return self.positions.copy() 