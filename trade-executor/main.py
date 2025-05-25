import asyncio
import json
import logging
import ccxt.async_support as ccxt
import aiokafka
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import signal
import sys
from contextlib import asynccontextmanager
import psycopg2
from confluent_kafka import Consumer, KafkaError
from prometheus_client import start_http_server

from config import config
from logger import logger
from metrics import TRADE_PROCESSING_TIME, TRADE_PROCESSING_ERRORS

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Инициализация FastAPI
app = FastAPI()

# Конфигурация Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092")
TRADE_COMMANDS_TOPIC = "trade-commands"
TRADE_EVENTS_TOPIC = "trade-events"

# Словарь для хранения экземпляров биржи для каждого пользователя
exchanges = {}

class TradeCommand(BaseModel):
    user_id: str
    symbol: str
    side: str
    size: float
    api_key: Optional[str] = None
    api_secret: Optional[str] = None

async def get_exchange(user_id: str, api_key: str, api_secret: str):
    """Получение или создание экземпляра биржи для пользователя"""
    if user_id not in exchanges:
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })
        exchanges[user_id] = exchange
    return exchanges[user_id]

async def execute_trade(command: TradeCommand, producer: aiokafka.AIOKafkaProducer):
    """Выполнение торговой операции"""
    try:
        exchange = await get_exchange(command.user_id, command.api_key, command.api_secret)
        
        # Проверка баланса
        balance = await exchange.fetch_balance()
        logger.info(f"Balance for user {command.user_id}: {balance}")
        
        # Выполнение сделки
        order = await exchange.create_order(
            symbol=command.symbol,
            type='market',
            side=command.side,
            amount=command.size
        )
        
        # Отправка события о выполнении сделки
        event = {
            'user_id': command.user_id,
            'symbol': command.symbol,
            'side': command.side,
            'size': command.size,
            'status': 'executed',
            'order_id': order['id'],
            'price': order['price']
        }
        await producer.send_and_wait(TRADE_EVENTS_TOPIC, json.dumps(event).encode())
        
        return order
        
    except Exception as e:
        logger.error(f"Error executing trade: {str(e)}")
        # Отправка события об ошибке
        error_event = {
            'user_id': command.user_id,
            'symbol': command.symbol,
            'side': command.side,
            'size': command.size,
            'status': 'error',
            'error': str(e)
        }
        await producer.send_and_wait(TRADE_EVENTS_TOPIC, json.dumps(error_event).encode())
        raise HTTPException(status_code=400, detail=str(e))

async def consume_trade_commands(producer: aiokafka.AIOKafkaProducer):
    """Потребление команд на выполнение сделок из Kafka"""
    consumer = aiokafka.AIOKafkaConsumer(
        TRADE_COMMANDS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="trade-executor-group"
    )
    
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                command_data = json.loads(msg.value.decode())
                command = TradeCommand(**command_data)
                await execute_trade(command, producer)
            except Exception as e:
                logger.error(f"Error processing trade command: {str(e)}")
    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()
    asyncio.create_task(consume_trade_commands(producer))

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}

class TradeExecutor:
    def __init__(self):
        self.consumer: Optional[Consumer] = None
        self.db_conn = None
        self.running = True

    async def setup(self):
        try:
            # Setup Kafka consumer
            self.consumer = Consumer({
                'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
                'group.id': config.KAFKA_CONSUMER_GROUP,
                'auto.offset.reset': 'earliest'
            })
            self.consumer.subscribe([config.KAFKA_TOPIC_TRADES])
            logger.info("Kafka consumer setup completed")

            # Setup database connection
            self.db_conn = psycopg2.connect(config.DATABASE_URL)
            logger.info("Database connection established")

            # Start Prometheus metrics server
            start_http_server(config.PROMETHEUS_PORT)
            logger.info(f"Prometheus metrics server started on port {config.PROMETHEUS_PORT}")

        except Exception as e:
            logger.error(f"Error during setup: {str(e)}")
            raise

    async def process_trade(self, trade_data):
        try:
            with TRADE_PROCESSING_TIME.time():
                # Process trade logic here
                logger.info(f"Processing trade: {trade_data}")
                # Add your trade processing logic here
        except Exception as e:
            TRADE_PROCESSING_ERRORS.inc()
            logger.error(f"Error processing trade: {str(e)}")
            raise

    async def run(self):
        try:
            await self.setup()
            logger.info("Trade executor started")

            while self.running:
                try:
                    msg = self.consumer.poll(1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            continue
                        logger.error(f"Kafka error: {msg.error()}")
                        continue

                    await self.process_trade(msg.value().decode('utf-8'))

                except Exception as e:
                    logger.error(f"Error in main loop: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            raise
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            if self.consumer:
                self.consumer.close()
            if self.db_conn:
                self.db_conn.close()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def handle_shutdown(self, signum, frame):
        logger.info("Shutdown signal received")
        self.running = False

async def main():
    executor = TradeExecutor()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, executor.handle_shutdown)
    signal.signal(signal.SIGTERM, executor.handle_shutdown)

    try:
        await executor.run()
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 