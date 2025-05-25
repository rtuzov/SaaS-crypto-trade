from binance.client import Client
import binance.enums as enums
import time
import requests
import telegram
import logging
import asyncio
import os
import sys


# Получение абсолютного пути к родительской директории
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавление родительской директории в sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Импортирование config модуля
try:
    from config import api_key2, api_secret2, FIXED_VOLUME2, cab2, counter2
except ImportError as e:
    print(f"Ошибка при импорте модуля config: {e}")
    sys.exit(1)
    

from config import api_key2, api_secret2, FIXED_VOLUME2, counter2, INITIAL_STOP_LOSS2, PROFIT_THRESHOLD2, TRAILING_STOP_INCREMENT2
from handlers.redis_handler import create_redis_connection, delete_key, save_to_redis_open_trade
    

# Настройка логирования
logger = logging.getLogger('monitor')
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Ваши API ключ и секрет
API_KEY = api_key2
API_SECRET = api_secret2

# Telegram Creds
TELEGRAM_BOT_TOKEN = '6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0'
TELEGRAM_CHAT_ID = '-1001998959723'

# Создание клиента API
client = Client(API_KEY, API_SECRET)

BASE_VALUE = FIXED_VOLUME2  # базовое значение позиции в долларах
INITIAL_STOP_LOSS = INITIAL_STOP_LOSS2  # начальный стоп-лосс в долларах
PROFIT_THRESHOLD = PROFIT_THRESHOLD2 # порог прибыли для изменения стоп-лосса в долларах
TRAILING_STOP_INCREMENT = TRAILING_STOP_INCREMENT2  # инкремент для трейлинг стопа


async def fetch_redis_keys():
    try:
        redis = await create_redis_connection(db=4)
        keys = await redis.keys('*')
        return keys
    except Exception as e:
        print(f"Error fetching Redis keys: {e}")
        return []


async def fetch_and_store_redis_keys():
    try:
        redis = await create_redis_connection(db=4)
        keys = await redis.keys('*')
        redis_data = {key: None for key in keys}
        return redis_data
    except Exception as e:
        print(f"Error fetching Redis keys: {e}")
        return {}

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

def get_open_positions():
    """
    Получение списка всех открытых позиций.
    """
    positions = client.futures_account()['positions']
    return [position for position in positions if float(position['positionAmt']) != 0]

def get_position_key(symbol, direction):
    """
    Создание уникального ключа для позиции в словаре stop_loss_dict.
    """
    return f"{symbol}_{direction}"


async def update_stop_loss(position, redis_keys, stop_loss, counter, anom):
    """
    Обновление стоп-лосса на основе нереализованной прибыли.
    """
    symbol = position['symbol']
    position_amt = float(position['positionAmt'])
    position_notional = float(position['notional'])
    init_margin = float(position['initialMargin'])
    direction = 'LONG' if position_notional > 0 else 'SHORT'
    key = get_position_key(symbol, direction)
    unrealized_profit = float(position['unrealizedProfit'])
#    basis_stop_loss_old = round((abs(position_notional) / 100) * INITIAL_STOP_LOSS, 2)
    basis_stop_loss = round(init_margin * INITIAL_STOP_LOSS, 5)

#    threshold_switch_old = round(abs(position_notional) / 100) * PROFIT_THRESHOLD

    threshold_switch = round(init_margin * PROFIT_THRESHOLD, 5)

    if unrealized_profit < threshold_switch:
        new_stop_loss = basis_stop_loss
        trail = 0

    else:

        stop_loss_pnl = unrealized_profit * TRAILING_STOP_INCREMENT
        new_stop_loss = max(stop_loss, stop_loss_pnl)
        trail = 1
    
    for k in redis_keys:
        if key in k:
            value = f"{position_amt}:{unrealized_profit}:{new_stop_loss}:{counter}:{anom}:{trail}"
            redis = await create_redis_connection(db=4)  # Создание подключения к Redis DB 4
            print(
                f"'Dual: Redis'{key} 'Amt:' {position_amt} 'Profit:' {unrealized_profit} 'SL:' {new_stop_loss} 'Counter:' {counter} 'Anomal:' {anom} 'Trail:' {trail}")
            await save_to_redis_open_trade(redis, k, value)
            logging.info(f"Updated Redis key {k} with value {value}")

    return new_stop_loss, trail, position_amt, unrealized_profit, counter, anom, trail

async def close_position(symbol, quantity, direction):
    """
    Закрытие позиции с учетом режима хеджирования.
    """

    try:
        side = enums.SIDE_SELL if direction == 'LONG' else enums.SIDE_BUY
        position_side = 'LONG' if direction == 'LONG' else 'SHORT'

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=enums.ORDER_TYPE_MARKET,
            quantity=quantity,
            positionSide=position_side
        )
        print("Позиция закрыта", order)

    except Exception as e:
        print(f"Ошибка при закрытии позиции: {e}")
        message = f"Ошибка при закрытии позиции: {e}"
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)


async def delete_matching_redis_keys(pattern):
    redis = await create_redis_connection(db=4)
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
        logging.info(f"Deleted keys: {keys}")

# Новый метод для сохранения ключа в Redis
async def save_custom_key_to_redis(custom_key, value):
    try:
        redis = await create_redis_connection(db=4)
        await save_to_redis_open_trade(redis, custom_key, value)
        logging.info(f"Saved custom key to Redis: {custom_key} with value: {value}")
    except Exception as e:
        logging.error(f"Error saving custom key to Redis: {e}")


async def monitor_and_manage_positions():
    while True:
        redis_keys = await fetch_and_store_redis_keys()
        open_positions = get_open_positions()
        
        global counter2, cab2
        
        cab = cab2
        counter = counter2
        for position in open_positions:
            symbol = position['symbol']
            position_amt = float(position['positionAmt'])
            direction = 'LONG' if position_amt > 0 else 'SHORT'
            key = get_position_key(symbol, direction)

            # Assuming 'cab' is a variable you have in your scope
            cab_value = str(cab2)  # Make sure it's a string if it's not already
            matching_key = next((k for k in redis_keys if key in k and cab_value in k), None)
            if matching_key:
                # print(f"'ключ' {matching_key}")
                redis = await create_redis_connection(db=4)
                value = await redis.get(matching_key)
                if value:
                    redis_value = parse_redis_value(value)
                    if redis_value['anom'] == 1:

                        new_stop_loss, trail, position_amt, unrealized_profit, counter, anom, trail = await update_stop_loss(
                            position, redis_keys, redis_value['stop_loss'],
                            redis_value['counter'], redis_value['anom'])

                       # Сохранение записи в Redis
                        value = f"{position_amt}:{unrealized_profit}:{new_stop_loss}:{counter}:{redis_value['anom']}:{trail}"
                        await save_to_redis_open_trade(redis, matching_key, value)
                        logging.info(f"Updated Redis key {matching_key} with value {value}")

                    if redis_value['counter'] >= counter2:
                        print(counter)
                        await close_position(symbol, abs(position_amt), direction)
                        message = f"{cab}: Закрытие позиции {symbol}, объемом {position_amt} в направлении {direction} по причине counter >= {counter2}, trail = {trail}, anom = {anom}, profit = {unrealized_profit}"
                        logging.info(message)
                        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
                        await delete_matching_redis_keys(f"*{key}*")
                        continue

                    redis_value = parse_redis_value(value)
                    new_stop_loss, trail, position_amt, unrealized_profit, counter, anom, trail = await update_stop_loss(
                        position, redis_keys, redis_value['stop_loss'],
                        redis_value['counter'], redis_value['anom'])


                    if unrealized_profit <= new_stop_loss:
                        counter += 1
                    else:
                        counter = 0

                    value = f"{position_amt}:{unrealized_profit}:{new_stop_loss}:{counter}:{redis_value['anom']}:{trail}"
                    await save_to_redis_open_trade(redis, matching_key, value)
                    logging.info(f"Updated Redis key {matching_key} with value {value}")

                    if unrealized_profit <= new_stop_loss and trail == 1:
                        await close_position(symbol, abs(position_amt), direction)
                        message = f"{cab}: Закрытие позиции {symbol}, объемом {position_amt} в направлении {direction} по причине достижения стоп-лосса {new_stop_loss}, trail = {trail}, anom = {anom}, profit = {unrealized_profit} "
                        logging.info(message)
                        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
                        await delete_matching_redis_keys(f"*{key}*")
                        continue
                else:
                    print(f"No value for key {matching_key}, using base values")
                    redis_value = {
                        'position_amt': position_amt,
                        'unrealized_profit': 0.0,
                        'stop_loss': -1.0,
                        'counter': 0,
                        'anom': 0,
                        'pnl': 0
                    }
                    await update_stop_loss(position, redis_keys, redis_value['stop_loss'],
                                           redis_value['counter'], redis_value['anom'])

            else:
                print('ключ не найден')
                trade_id = "None"
                direction1 = 'LONG' if direction == 'LONG' else 'SHORT'
                cab = cab2
                custom_key = f"{symbol}_{direction1}:{trade_id}:{symbol}:{direction}:{cab}"
                await save_custom_key_to_redis(custom_key, "")
                redis_keys = await fetch_and_store_redis_keys()
                await update_stop_loss(position, redis_keys, -1, 0, 0)
        print('-------------------')
        time.sleep(2)


asyncio.run(monitor_and_manage_positions())
