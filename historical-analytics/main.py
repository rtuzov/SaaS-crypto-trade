import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    asyncio.create_task(consume_trade_events())
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/trading"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = "redpanda:9092"
TRADE_EVENTS_TOPIC = "trade-events"

class TradeAnalytics:
    def __init__(self):
        self.trades_df = pd.DataFrame()
        
    async def load_trades(self, user_id: str, start_date: Optional[datetime] = None):
        async with async_session() as session:
            query = text("""
                SELECT * FROM trades 
                WHERE user_id = :user_id 
                AND timestamp >= :start_date
                ORDER BY timestamp
            """)
            result = await session.execute(query, {
                "user_id": user_id,
                "start_date": start_date or (datetime.now() - timedelta(days=30))
            })
            trades = result.fetchall()
            
            self.trades_df = pd.DataFrame(trades)
            if not self.trades_df.empty:
                self.trades_df['timestamp'] = pd.to_datetime(self.trades_df['timestamp'])
    
    def calculate_metrics(self) -> Dict:
        if self.trades_df.empty:
            return {}
            
        total_trades = len(self.trades_df)
        winning_trades = len(self.trades_df[self.trades_df['pnl'] > 0])
        losing_trades = len(self.trades_df[self.trades_df['pnl'] < 0])
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": winning_trades / total_trades if total_trades > 0 else 0,
            "total_pnl": self.trades_df['pnl'].sum(),
            "avg_pnl": self.trades_df['pnl'].mean(),
            "max_drawdown": self.calculate_max_drawdown(),
            "sharpe_ratio": self.calculate_sharpe_ratio()
        }
    
    def calculate_max_drawdown(self) -> float:
        if self.trades_df.empty:
            return 0.0
            
        cumulative = self.trades_df['pnl'].cumsum()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return abs(drawdown.min())
    
    def calculate_sharpe_ratio(self) -> float:
        if self.trades_df.empty:
            return 0.0
            
        returns = self.trades_df['pnl'].pct_change().dropna()
        if len(returns) < 2:
            return 0.0
            
        return np.sqrt(252) * returns.mean() / returns.std()

analytics = TradeAnalytics()

async def consume_trade_events():
    consumer = AIOKafkaConsumer(
        TRADE_EVENTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="historical-analytics"
    )
    
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                trade_data = json.loads(msg.value.decode())
                # Store trade in database
                async with async_session() as session:
                    query = text("""
                        INSERT INTO trades (
                            id, user_id, symbol, side, size, 
                            entry_price, exit_price, pnl, timestamp
                        ) VALUES (
                            :id, :user_id, :symbol, :side, :size,
                            :entry_price, :exit_price, :pnl, :timestamp
                        )
                    """)
                    await session.execute(query, trade_data)
                    await session.commit()
                    
            except Exception as e:
                logger.error(f"Error processing trade event: {str(e)}")
                
    finally:
        await consumer.stop()

@app.get("/api/analytics/{user_id}")
async def get_analytics(
    user_id: str,
    start_date: Optional[datetime] = None
):
    try:
        await analytics.load_trades(user_id, start_date)
        return analytics.calculate_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 