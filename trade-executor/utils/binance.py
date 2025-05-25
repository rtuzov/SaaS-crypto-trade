import ccxt
import asyncio
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
                'recvWindow': 5000
            }
        })
        
    async def get_balance(self) -> Dict[str, float]:
        try:
            balance = await self.exchange.fetch_balance()
            return {
                'free': float(balance['USDT']['free']),
                'used': float(balance['USDT']['used']),
                'total': float(balance['USDT']['total'])
            }
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            raise
            
    async def create_order(self, symbol: str, side: str, amount: float, leverage: int) -> Dict:
        try:
            # Set leverage
            await self.exchange.set_leverage(leverage, symbol)
            
            # Create order
            order = await self.exchange.create_order(
                symbol=symbol,
                type='market',
                side=side.lower(),
                amount=amount
            )
            
            return {
                'id': order['id'],
                'status': order['status'],
                'price': float(order['price']),
                'amount': float(order['amount']),
                'cost': float(order['cost']),
                'timestamp': datetime.fromtimestamp(order['timestamp'] / 1000)
            }
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
            
    async def cancel_order(self, order_id: str, symbol: str) -> bool:
        try:
            await self.exchange.cancel_order(order_id, symbol)
            return True
        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            return False
            
    async def get_order_status(self, order_id: str, symbol: str) -> Optional[Dict]:
        try:
            order = await self.exchange.fetch_order(order_id, symbol)
            return {
                'id': order['id'],
                'status': order['status'],
                'price': float(order['price']),
                'amount': float(order['amount']),
                'cost': float(order['cost']),
                'timestamp': datetime.fromtimestamp(order['timestamp'] / 1000)
            }
        except Exception as e:
            logger.error(f"Error fetching order status: {e}")
            return None 