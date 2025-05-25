import asyncio
import json
import logging
from datetime import datetime
from handlers.redis_handler import create_redis_connection, save_to_redis, get_value, get_all_keys, delete_key
from handlers.telegram_bot import send_to_error
from handlers.message_handler import process_message

# Создание логгера
logger = logging.getLogger('my_bot')

# Настройка логгирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Установка уровня логирования
logger.setLevel(logging.ERROR)

# Создание и настройка консольного обработчика (handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Добавление обработчика к логгеру
logger.addHandler(console_handler)

# Теперь можно использовать logger
logger.info("Logging setup complete.")


async def check_redis_records_periodically():
    while True:
        try:
            logger.info("Checking Redis records...")
            await check_redis_records()
            logger.info("Checked Redis records successfully.")
        except Exception as e:
            logger.error(f"Error while checking Redis records check_redis_records_periodically: {e}")
            error = f"Error while checking Redis records check_redis_records_periodically: {e}"
            await send_to_error(error)

        await asyncio.sleep(30)


async def check_redis_records():
    try:
        redis_queue = await create_redis_connection(db=1)
        redis_sql = await create_redis_connection(db=2)
          # Указываем 1 для подключения к первой базе данных
        keys = await get_all_keys(redis_queue)
        keys.reverse()
        if keys:
            for key in keys:
                try:
                    redis_value = await get_value(redis_queue, key)
                    values = redis_value.split("|")
                    logger.info(f"Processing key: {key}, values: {values}")
                    message_date, chat_id, chat_title, message_id, text, cat = values
                    title = chat_title
                    
                    chat_id = int(chat_id)
                    # Only process message if 'text' is not empty
                    if text.strip():  # Checking if text is not just whitespace
                        checker = 'checker'
                        await process_message(redis_sql, text.lower().replace('\n', ' '), cat, chat_title, chat_id, message_id, text, checker)
                    else:
                        await delete_key(redis_queue, key)  # Delete the key if text is empty
                        logger.info(f"Deleted key {key} as text was empty.")
                except Exception as e:
                    if "WRONGTYPE Operation against a key holding the wrong kind of value" not in str(e):
                        logger.error(f"Error while processing key {key}: {e}")
                        error = f"Error while processing key {key}: {e}"
                        await send_to_error(error)
        else:
            logger.info("No keys found in Redis.")
    except Exception as e:
        logger.error("Error while checking Redis records: %s", e)
        error = f"Error while checking Redis records: {e} {key}"
        await send_to_error(error)


async def main():
    logger.info("Starting Redis checker...")
    await asyncio.create_task(check_redis_records_periodically())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Redis checker stopped.")
        error = f"Redis checker stopped."
        send_to_error(error)
