from binance.client import Client
from config import api_key1, api_secret1, FIXED_VOLUME1, cab1, close_option1
import asyncio
import time
from handlers.redis_handler import create_redis_connection, save_to_redis, get_value, get_all_keys, delete_key
from handlers.telegram_bot import check_binance_tg
from telegram import Bot

# Введите свои API ключи
api_key = api_key1
secret_key = api_secret1

# Создаем объект клиента Binance
client = Client(api_key, secret_key)


close_option = close_option1

# Функция для получения всех ключей из Redis
async def fetch_redis_keys():
    try:
        redis_conn = await create_redis_connection(db=4)
        keys = await redis_conn.keys('*')
        return keys
    except Exception as e:
        print(f"Error fetching Redis keys: {e}")
        return []

# Функция для получения всех данных из Redis и их обновления
async def fetch_and_store_redis_keys():
    try:
        redis_conn = await create_redis_connection(db=4)
        keys = await redis_conn.keys('*')
        redis_data = {}
        for key in keys:
            value = await redis_conn.get(key)
            if value:
                redis_data[key] = parse_redis_value(value)
                # Обновляем поле anom
                redis_data[key]['anom'] = 1
                # Сохраняем обратно в Redis
                await redis_conn.set(key, serialize_redis_value(redis_data[key]))
        return redis_data
    except Exception as e:
        print(f"Error fetching Redis keys: {e}")
        return {}

# Функция для преобразования значения из Redis в словарь
def parse_redis_value(value):
    """
    Преобразование строки значения Redis в словарь.
    """
    parts = value.split(':')
    return {
        'position_amt': float(parts[0]),
        'unrealized_profit': float(parts[1]),
        'stop_loss': float(parts[2]),
        'counter': int(parts[3]),
        'anom': int(parts[4]),
        'trail': int(parts[5])
    }

# Функция для сериализации словаря в строку
def serialize_redis_value(data):
    """
    Преобразование словаря в строку для хранения в Redis.
    """
    return f"{data['position_amt']}:{data['unrealized_profit']}:{data['stop_loss']}:{data['counter']}:{data['anom']}:{data['trail']}"

# Основной код для выгрузки и сохранения данных
async def main():
    try:
        # Получаем баланс аккаунта
        balance = client.futures_account()

        # Извлекаем необходимые значения
        total_margin_balance = float(balance['totalMarginBalance'])
        total_wallet_balance = float(balance['totalWalletBalance'])

        margin = round(total_margin_balance / total_wallet_balance, 2)

        margin2 = total_margin_balance - total_wallet_balance
        print(f"-------- Коэф = {margin} --------")
        print(f"-------- Коэф = {margin2} --------")
        # Если value больше 1.2, обрабатываем данные в Redis
        if margin >= close_option or margin2 >= 23:
            print(margin, close_option)
            await fetch_and_store_redis_keys()
            await check_binance_tg(f"Аномалия 1 проставлена, ждем закрытия позиций. Отношение баланса кабинета к марже: {margin}")

       # else:
           # await check_binance_tg(f"Отношение баланса кабинета к марже: {margin}")

    except Exception as e:
        await check_binance_tg(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

async def periodic_main(interval):
    while True:
        await main()
        await asyncio.sleep(interval)

if __name__ == '__main__':
    asyncio.run(periodic_main(2))