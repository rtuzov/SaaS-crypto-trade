from binance.client import Client
from binance.enums import *
import logging
from datetime import datetime
from handlers.telegram_bot import send_to_error, open_trade_tg
import asyncio
from config import api_key2, api_secret2, FIXED_VOLUME2, cab2
from handlers.redis_handler import create_redis_connection, save_to_redis_trade, get_value, get_all_keys, delete_key, save_to_redis_coin
from binance.exceptions import BinanceAPIException
import requests

"""
Как использовать?
order = open_futures_trade('12345', 'XRPUSDT', 'buy', 250)
Данные должны передваться в эту фунцию вместе а айди сделки в виде айди канала + сообщения.
Размер позы тоже передается в зависимости от акка

Логи пишутся в один файл
Можно идентифицировать счета по размеру позы
"""

fixed_volume = FIXED_VOLUME2

# Настройка логирования
logger = logging.getLogger('my_bot')
logging.basicConfig(filename='futures_trades_NEW_TEST.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Параметры API
api_key = api_key2
api_secret = api_secret2

cab = cab2

# Создание клиента API для работы с USDⓈ-M фьючерсами
client = Client(api_key, api_secret)

keywords_buy = ['long', 'buy', 'покупка']
keywords_sell = ['short', 'sell', 'продажа']

def contains_keyword(direction, keywords):
    direction_lower = direction.lower()
    return any(keyword in direction_lower for keyword in keywords)

def get_asset_precision(symbol):
    try:
        if symbol in ["TONUSDT", "BSVUSDT"]:
            return 1

        if symbol in ["MYROUSDT", "KASUSDT", "TURBOUSDT", "1000RATSUSDT", "1000SHIB", "1000XEC", "1000LUNC", "1000PEPE", "1000FLOKI", "1000BONC", "1000SATS", "BIGTIMEUSDT", "MEWUSDT", "ORBSUSDT"]:
            return 0         
        
        info = client.get_symbol_info(symbol)

        
        for filter in info['filters']:
            if filter['filterType'] == 'LOT_SIZE':
                return filter['stepSize'].find('1')
    except Exception as e:
        logging.error(f"Error fetching asset precision for {symbol}: {e}")
    
    return -1

def calculate_quantity(symbol, precision):
    try:
#        if symbol in ["1000PEPEUSDT", "1000LUNCUSDT"]:
#            symbol = symbol.replace('1000', '')

#        ticker_info = client.get_symbol_ticker(symbol=symbol)
#        if 'price' not in ticker_info:
#            raise ValueError(f"Price information not found for symbol: {symbol}")

        url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
        params = {'symbol': symbol}
        response = requests.get(url, params=params)


        if response.status_code == 200:
            data = response.json()
            mark_price = data['markPrice']
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        price = float(mark_price)

        quantity = fixed_volume / price

        rounded_quantity = round(quantity, precision)
        return rounded_quantity

    except Exception as e:
        logging.error(f"Error calculating quantity for {symbol}: {e}")
        return 0

async def save_trade(trade_id, symbol, direction, filename):
    try:
        with open(filename, 'a') as f:
            f.write(f"{datetime.now()}, {trade_id}, {symbol}, {direction}, {cab}\n")
    except Exception as e:
        logging.error(f"Error writing trade to file {filename}: {e} {trade_id}")
        await send_to_error(f"Error writing trade to file {filename}: {e} {trade_id}")

async def save_trade_to_redis(redis, trade_id, symbol, direction, cab):
    try:
        direction1 = direction.upper()
        redis_key = f"{symbol}_{direction1}:{trade_id}:{symbol}:{direction}:{cab}"

        await save_to_redis_trade(redis, redis_key)
    except Exception as e:
        logging.error(f"Error saving trade to Redis: {e} {trade_id}")
        await send_to_error(f"Error saving trade to Redis: {e} {trade_id}")

async def open_futures_trade_third(trade_id, symbol, direction, chat_id, message_id):
    try:
        symbol = symbol.upper().replace(" ", "").replace("/", "") + "USDT"
		
        precision = get_asset_precision(symbol)

        # Static precision values for specific symbols
        static_precisions = {
            "SOLUSDT": 0,
            "AVAXUSDT": 0,
            "JOEUSDT": 0,
            "ORDIUSDT": 0,
            "BTCUSDT": 3,
            "ETHUSDT": 3,
            "DYDXUSDT": 1,
            "APTUSDT": 1,
            "EGLDUSDT": 0,
            "1000PEPEUSDT": 0,
        }

        # Static minimum quantity values for specific symbols
        static_min_quantities = {
            "JOEUSDT": 11,
            "ORDIUSDT": 0.1,
            "BTCUSDT": 0.002,
            "ETHUSDT": 0.006,
            "DYDXUSDT": 2.6,
            "APTUSDT": 0.6,
            "EGLDUSDT": 0.2,
            "TRUUSDT": 27,
            "BLZUSDT": 20,
            "ETHFIUSDT": 1.1,
            "1000PEPEUSDT": 336,
            "IOTAUSDT": 22.5,
            "GALAUSDT": 111,
            "CKBUSDT": 318,
            "DUSKUSDT": 11,
            "COTIUSDT": 35,
            "IOTXUSDT": 85,
            "GRTUSDT": 17,
            "ALGOUSDT": 27.3,
            "MANAUSDT": 11,
            "FRONTUSDT": 4,
            "HBARUSDT": 50,
            "TRBUSDT": 0.1,            
            "TONUSDT": 0.8,
            "MYROUSDT": 19,
            "KASUSDT": 27,
            "TURBOUSDT": 834,
            "1000RATSUSDT": 30,
            "BSVUSDT": 0.1,
            "BIGTIMEUSDT": 25,
            "MEWUSDT": 30,
            "ORBSUSDT": 173
        }

        if symbol in static_precisions:
            precision = static_precisions[symbol]

        if precision == -1:
            raise ValueError(f"Invalid precision for symbol: {symbol}")

        while precision >= 0:
            try:
                quantity = calculate_quantity(symbol, precision)

               # Adjust quantity based on static minimum values
                if symbol in static_min_quantities:
                    quantity = max(static_min_quantities[symbol], round(quantity, precision))

                redis_queue = await create_redis_connection(db=1)
                redis_key = f"{chat_id}:{message_id}"
                await delete_key(redis_queue, redis_key)                
                
                order = client.futures_create_order(
                    symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='SHORT'
                )

                direction = 'short'
                logging.info(f"Trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, "
                             f"Time: {datetime.now()}, Order Details: {order}")

                await save_trade(trade_id, symbol, direction, 'successful_trades.txt')

                redis_monitor = await create_redis_connection(db=4)  # Создание подключения к Redis DB 4
                await save_trade_to_redis(redis_monitor, trade_id, symbol, direction, cab)
                
                symbol = symbol.replace('USDT', '')
                redis_duplicate = await create_redis_connection(db=3)  # Создание подключения к Redis DB 3
                redis_key = f"{symbol}_{direction}"
                redis_value = f"{message_id}_{chat_id}"
                ttl = 300  # Время жизни ключа в секундах (5 минут)

                await save_to_redis_coin(redis_duplicate, redis_key, redis_value)
                await redis_duplicate.expire(redis_key, ttl)  # Установка времени жизни ключа на 5 минут
                
                await open_trade_tg(f"Opened trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, Cab: {cab}")
                return order

            except BinanceAPIException as e:
                if 'APIError(code=-1111)' in str(e):
                    precision -= 1
                    logging.error(f"Reducing precision for {symbol} due to APIError -1111. New precision: {precision}")
                else:
                    raise e

        if precision < 0:
            raise ValueError(f"Failed to open trade for symbol: {symbol}. Precision reduced below zero.")

    except Exception as e:
        logging.error(f"Error opening trade: {trade_id}, Symbol: {symbol}, Direction: {direction}, Error: {e}")
        await save_trade(trade_id, symbol, direction, 'failed_trades.txt')
        await send_to_error(f"Error opening trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, Error: {e}, Cab: {cab}")
        raise


# Пример использования
async def main():
    try:
        current_mode = client.futures_get_position_mode()
        print(current_mode)
        # order = await open_futures_trade('12345', 'XRPUSDT', 'buy', 250)  # Пример сделки
        # print(order)
    except Exception as e:
        logging.error(e)
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
