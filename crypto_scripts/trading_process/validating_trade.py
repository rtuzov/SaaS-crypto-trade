#from trading_process.trading_open_test_002_RT import open_futures_position1 - без хэджирования
#from trading_process.trading_open_test_002_RT_v2 import open_futures_position2 - без хэджирования
            # Тут должен быть вызов функции открытия позиции:
            #open_futures_position(message_id, coin, direction)
            #open_futures_trade_second(message_id, coin, direction)
            #open_futures_trade_third(message_id, coin, direction)
import os
import sys
import csv
import logging
from collections import OrderedDict
from datetime import datetime
import aiofiles
from handlers.redis_handler import create_redis_connection, save_to_redis, get_value, get_all_keys, delete_key,save_to_redis_coin
from handlers.telegram_bot import send_to_channel_links, send_to_channel_spot, send_to_main_channel, send_to_channel, send_to_error
from trading_process.open_positions_basic import open_futures_trade as open_futures_position
from trading_process.open_positions_dual_long import open_futures_trade_second as open_futures_trade_second
from trading_process.open_positions_dual_short import open_futures_trade_third as open_futures_trade_third

# Настройка логирования
logger = logging.getLogger('my_bot')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Используем OrderedDict для хранения пар монета-направление с учётом порядка добавления
recent_trades = OrderedDict()
max_trades = 5  # Максимальное количество сохраняемых торгов

async def read_authorized_channels():
    try:
        #async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'authorized_channels.txt'), 'r') as file:
        #        async with aiofiles.open(os.path.join(os.path.dirname(__file__), 'authorized_channels.txt'), 'r') as file:
        async with aiofiles.open('/opt/my_test/fully_automated_analytics/strategy1/filter.txt', 'r') as file:
             return [line.strip() for line in await file.readlines()]
    except Exception as e:
        logging.error(f"Error reading authorized channels: {e}")
        error = f"Error reading authorized channels: {e}"
        await send_to_error(error)
        return []

async def is_channel_authorized(chat_id):
    chat_id = abs(chat_id)
    authorized_channels = await read_authorized_channels()
    return str(chat_id) in authorized_channels

async def save_unauthorized_trade(chat_id, message_id, coin, direction):
    try:
        async with aiofiles.open('/opt/my_test/trading_process/unauthorized_to_trade.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            await file.write(','.join([str(datetime.now()), str(chat_id), str(message_id), coin, direction]) + '\n')
    except Exception as e:
        logging.error(f"Error saving unauthorized trade: {e}")
        error = f"Error saving unauthorized trade: {e}"
        await send_to_error(error)

async def authorized_trades_with_id(chat_id, message_id, coin, direction):
    try:
        async with aiofiles.open('/opt/my_test/trading_process/authorized_trades_with_id.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            await file.write(','.join([str(datetime.now()), str(chat_id), str(message_id), coin, direction]) + '\n')
    except Exception as e:
        logging.error(f"Error saving authorized trade: {e}")
        error = f"Error saving authorized trade: {e}"
        await send_to_error(error)


async def process_trade(chat_id, message_id, coin, direction):

        # List of blocked coins
    blocked_coins = ['TNETUSDT', 'SLERFUSDT', 'TНЕТАUSDT', 'TNB', 'MFG', 'RONUSDT', 'ADAID', 'ADAETH', 'ADAXXX', 'MEW', 'MOG', 'ZEUS']

    # Check if the coin is blocked for trading
    if any(blocked_coin in coin for blocked_coin in blocked_coins):
        error = f"Coin {coin} is blocked for trading."
        await send_to_error(error)  # Ensure this function is defined to handle errors
        redis_queue = await create_redis_connection(db=1)
        redis_key = f"{chat_id}:{message_id}"
        await delete_key(redis_queue, redis_key)
        return  # Exit the function to stop further processing
    
    if 'long' in direction:
        direction = 'long'
    else:
        direction = 'short'
        
    redis = await create_redis_connection(db=3)  # Создание подключения к Redis DB 3
    redis_key = f"{coin}_{direction}"

    if await is_channel_authorized(chat_id):
        logger.info(f'Channel {chat_id} is authorized.')
        await authorized_trades_with_id(chat_id, message_id, coin, direction)
		

        existing = await get_value(redis, redis_key)
        
        if not existing:
            logger.info(f"Trade opened for {coin} in {direction} direction. Saved to Redis.")
            trade_id =  f"{chat_id}_{message_id}"

            await open_futures_position(trade_id, coin, direction, chat_id, message_id)
           # await open_futures_trade_second(trade_id, coin, direction, chat_id, message_id)
           # await open_futures_trade_third(trade_id, coin, direction, chat_id, message_id)
            # Здесь могут быть вызовы функций для открытия позиции
            
        else:
            logger.info(f"Trade for {coin} in {direction} direction already exists. Skipping.")
            error = f"Trade for {coin} in {direction} direction already exists. Skipping."
            await send_to_error(error)  # Убедитесь, что функция send_to_error определена
    else:
        logger.warning(f'Channel {chat_id} failed authorization.')
        await save_unauthorized_trade(chat_id, message_id, coin, direction)
        #error = f'Channel {chat_id} failed authorization.'
        #await send_to_error(error)