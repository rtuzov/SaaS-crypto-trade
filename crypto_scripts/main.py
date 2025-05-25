import os
import asyncio
import logging
import signal
from telethon import TelegramClient, events, functions
from config import API_ID, API_HASH, TOKEN, TOKEN1
from handlers.telegram_bot import send_to_channel_links, send_to_channel_spot, send_to_main_channel, send_to_channel, send_to_error
from handlers.message_handler import handle_text_messages

# Настройка логирования
logger = logging.getLogger('my_bot')
logger.setLevel(logging.ERROR)

# Логирование в файл
file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Логирование на экран (консоль)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Проверка существования директории для файла сессии
session_dir = '/opt/my_test/'
os.makedirs(session_dir, exist_ok=True)
session_name = os.path.join(session_dir, 'session_name_unique')
logger.error(f"Attempting to access session file at: {os.path.abspath(session_name)}.session")

# Создание клиента с обработкой ошибок
try:
    client = TelegramClient(session_name, API_ID, API_HASH, device_model='My Device', system_version='1.0',
                            app_version='1.0', lang_code='en')
    logger.info("Telegram client successfully created.")
except Exception as e:
    logger.error(f"Failed to create TelegramClient session: {str(e)}")


@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text
    chat_id = event.chat_id
    text_replace = text.lower().replace('|', '\\')
    text_original = text.replace('|', '\\')
    chat_title_base = (await event.get_chat()).title if event.is_group or event.is_channel else "Private Chat"
    chat_title = chat_title_base.replace('|', '\\')
    message_id = event.id
    message_date = event.date
    formatted_date = message_date.strftime('%Y-%m-%d %H:%M:%S')

    await handle_text_messages(event, text, chat_id, text_replace, text_original, chat_title, message_id, formatted_date)


async def main():
    # Запуск клиента с обработкой ошибок подключения
    try:
        await client.start()
        print("Client Created and Logged in")
        logger.info("Client logged in successfully.")
    except Exception as e:
        logger.error(f"Failed to start client: {str(e)}")
        return

    # Вывод информации о сессиях
    try:
        sessions = await client(functions.account.GetAuthorizationsRequest())
        for session in sessions.authorizations:
            logger.info(f"Session ID: {session.hash}")
            logger.info(f"Device Model: {session.device_model}")
            logger.info(f"Platform: {session.platform}")
            logger.info(f"App Name: {session.app_name}")
            logger.info(f"App Version: {session.app_version}")
            logger.info(f"System Version: {session.system_version}")
            logger.info(f"Country: {session.country}")
            logger.info(f"IP: {session.ip}")
            logger.info(f"Region: {session.region}")
            logger.info(f"Date Created: {session.date_created}")
            logger.info(f"Date Active: {session.date_active}")
            logger.info(f"Last Active IP: {session.ip}")
            logger.info("---------------")
    except Exception as e:
        logger.error(f"Failed to retrieve session info: {str(e)}")

    # Оставляем клиента работать до отключения
    await client.run_until_disconnected()


# Корректное завершение работы клиента
async def shutdown():
    await client.disconnect()
    print("Client disconnected")
    logger.info("Client disconnected.")

# Добавляем обработку сигналов для корректного завершения
client.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown()))
client.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown()))

# Запуск основной функции
try:
    client.loop.run_until_complete(main())
except Exception as e:
    logger.error(f"Unexpected error occurred: {str(e)}")
finally:
    client.loop.run_until_complete(shutdown())
