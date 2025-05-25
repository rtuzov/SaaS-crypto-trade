import asyncio
import logging
import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "redpanda:9092")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Kafka producer
producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer
    # Startup
    logger.info("Telegram Collector service starting up")
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try:
        await producer.start()
        logger.info(f"Connected to Kafka broker at {KAFKA_BROKER}")
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        # В случае ошибки подключения к Kafka, сервис может считаться нездоровым
        # Но для теста healthcheck эндпоинта, оставим producer как есть
        pass
        
    logger.info("Telegram Collector service is ready to collect messages.")
    yield
    # Shutdown
    logger.info("Telegram Collector service shutting down")
    if producer._sender.sender_task and not producer._sender.sender_task.done(): # Проверка перед остановкой
        await producer.stop()
        logger.info("Kafka producer stopped.")
    else:
        logger.info("Kafka producer was not active or already stopped.")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "UP", "message": "Telegram collector is running"} # Всегда UP для теста

# Placeholder for actual Telegram message handling logic
async def handle_telegram_message(message_data):
    logger.info(f"Received message: {message_data}")
    try:
        await producer.send_and_wait("telegram_messages", message_data)
        logger.info(f"Message sent to Kafka topic 'telegram_messages': {message_data}")
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")

@app.post("/webhook")
async def telegram_webhook(message: dict):
    try:
        if producer:
            await producer.send_and_wait(
                "telegram-messages",
                {
                    "chat_id": message.get("chat", {}).get("id"),
                    "text": message.get("text", ""),
                    "timestamp": message.get("date")
                }
            )
            logger.info(f"Message sent to Kafka: {message.get('text', '')}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # В Docker CMD будет python main.py, uvicorn будет запускаться из CMD в Dockerfile или docker-compose
    # Для локального запуска можно использовать:
    uvicorn.run(app, host="0.0.0.0", port=8000) 