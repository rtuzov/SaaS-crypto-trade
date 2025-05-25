import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class TradeAnalyzer:
    def __init__(self):
        self.successful_trades = pd.DataFrame()
        self.failed_trades = pd.DataFrame()
        
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
            
            df = pd.DataFrame(trades)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                # Разделяем на успешные и неуспешные сделки
                self.successful_trades = df[df['pnl'] > 0]
                self.failed_trades = df[df['pnl'] <= 0]
    
    def analyze_trades(self) -> Dict:
        if self.successful_trades.empty and self.failed_trades.empty:
            return {}
            
        total_trades = len(self.successful_trades) + len(self.failed_trades)
        win_rate = len(self.successful_trades) / total_trades if total_trades > 0 else 0
        
        # Анализ успешных сделок
        successful_analysis = {
            "count": len(self.successful_trades),
            "avg_profit": self.successful_trades['pnl'].mean(),
            "max_profit": self.successful_trades['pnl'].max(),
            "avg_duration": (self.successful_trades['exit_time'] - self.successful_trades['timestamp']).mean().total_seconds() / 3600,  # в часах
            "best_symbols": self.successful_trades.groupby('symbol')['pnl'].sum().nlargest(3).to_dict()
        }
        
        # Анализ неуспешных сделок
        failed_analysis = {
            "count": len(self.failed_trades),
            "avg_loss": self.failed_trades['pnl'].mean(),
            "max_loss": self.failed_trades['pnl'].min(),
            "avg_duration": (self.failed_trades['exit_time'] - self.failed_trades['timestamp']).mean().total_seconds() / 3600,  # в часах
            "worst_symbols": self.failed_trades.groupby('symbol')['pnl'].sum().nsmallest(3).to_dict()
        }
        
        return {
            "total_trades": total_trades,
            "win_rate": win_rate,
            "successful_trades": successful_analysis,
            "failed_trades": failed_analysis,
            "profit_factor": abs(self.successful_trades['pnl'].sum() / self.failed_trades['pnl'].sum()) if len(self.failed_trades) > 0 else float('inf'),
            "avg_trade": (self.successful_trades['pnl'].sum() + self.failed_trades['pnl'].sum()) / total_trades if total_trades > 0 else 0
        } 