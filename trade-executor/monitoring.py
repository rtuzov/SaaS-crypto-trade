import asyncio
import logging
from typing import Dict, Any
import ccxt.async_support as ccxt
from aiokafka import AIOKafkaProducer
import json
import time

logger = logging.getLogger(__name__)

class BalanceMonitor:
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self.producer = kafka_producer
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self.close_option = 1.2  # Порог для закрытия позиций
        
    async def get_exchange(self, user_id: str, api_key: str, api_secret: str) -> ccxt.Exchange:
        if user_id not in self.exchanges:
            exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
            })
            self.exchanges[user_id] = exchange
        return self.exchanges[user_id]
        
    async def check_balance(self, user_id: str, api_key: str, api_secret: str):
        try:
            exchange = await self.get_exchange(user_id, api_key, api_secret)
            balance = await exchange.fetch_balance()
            
            total_margin_balance = float(balance['total']['marginBalance'])
            total_wallet_balance = float(balance['total']['walletBalance'])
            
            margin = round(total_margin_balance / total_wallet_balance, 2)
            margin_diff = total_margin_balance - total_wallet_balance
            
            if margin >= self.close_option or margin_diff >= 23:
                # Отправляем событие в Kafka
                await self.producer.send(
                    'balance-alerts',
                    key=user_id.encode(),
                    value=json.dumps({
                        'user_id': user_id,
                        'margin_ratio': margin,
                        'margin_diff': margin_diff,
                        'timestamp': int(time.time() * 1000)
                    }).encode()
                )
                
                logger.warning(f"Balance anomaly detected for user {user_id}: margin={margin}, diff={margin_diff}")
                
        except Exception as e:
            logger.error(f"Error checking balance for user {user_id}: {str(e)}")
            
    async def start_monitoring(self, interval: int = 60):
        while True:
            # Получаем список пользователей из базы данных
            # TODO: Implement user list retrieval
            for user in users:
                await self.check_balance(
                    user['id'],
                    user['api_key'],
                    user['api_secret']
                )
            await asyncio.sleep(interval) 