from binance.client import Client
from binance.enums import *
import logging
from datetime import datetime
from handlers.telegram_bot import send_to_error, open_trade_tg
import asyncio
from config import api_key1, api_secret1, FIXED_VOLUME1, cab1
from handlers.redis_handler import create_redis_connection, save_to_redis_trade


"""
Как использовать?
order = open_futures_trade('12345', 'XRPUSDT', 'buy', 250)
Данные должны передваться в эту фунцию вместе а айди сделки в виде айди канала + сообщения.
Размер позы тоже передается в зависимости от акка

Логи пишутся в один файл
Можно идентифицировать счета по размеру позы
"""

fixed_volume = FIXED_VOLUME1

# Настройка логирования
logger = logging.getLogger('my_bot')
logging.basicConfig(filename='futures_trades_NEW_TEST.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Параметры API
api_key = api_key1
api_secret = api_secret1

cab = cab1


# Создание клиента API для работы с USDⓈ-M фьючерсами
client = Client(api_key, api_secret)

keywords_buy = ['long', 'buy', 'покупка']
keywords_sell = ['short', 'sell', 'продажа']

def contains_keyword(direction, keywords):
    direction_lower = direction.lower()
    return any(keyword in direction_lower for keyword in keywords)

def get_asset_precision(symbol):
    try:
        info = client.get_symbol_info(symbol)
        for filter in info['filters']:
            if filter['filterType'] == 'LOT_SIZE':
                return filter['stepSize'].find('1') - 1
    except Exception as e:
        logging.error(f"Error fetching asset precision for {symbol}: {e}")
    return -1

def get_max_precision(symbol):
    try:
        info = client.get_symbol_info(symbol)
        for filter in info['filters']:
            if filter['filterType'] == 'LOT_SIZE':
                step_size = float(filter['stepSize'])
                max_precision = abs(('%f' % step_size).find('1') - 1)
                return max_precision
    except Exception as e:
        logging.error(f"Error fetching max precision for {symbol}: {e}")
    return -1
def calculate_quantity(symbol):
    try:
        if symbol in ["1000PEPEUSDT", "1000LUNCUSDT"]:
            symbol = symbol.replace('1000', '')

        precision = get_asset_precision(symbol)
        max_precision = get_max_precision(symbol)
        ticker_info = client.get_symbol_ticker(symbol=symbol)
        print(ticker_info)
        if 'price' not in ticker_info:
            raise ValueError(f"Price information not found for symbol: {symbol}")

        price = float(ticker_info['price'])
        print(price)

        if symbol in ["SOLUSDT", "AVAXUSDT"]:
            precision = 0

        elif symbol == "JOEUSDT":
            precision = 0
            quantity = fixed_volume / price
            return max(11, round(quantity, precision))

        elif symbol == "ORDIUSDT":
            precision = 0
            quantity = fixed_volume / price
            return max(0.1, round(quantity, precision))

        elif symbol == "BTCUSDT":
            precision = get_asset_precision(symbol)
            quantity = fixed_volume / price
            return max(0.002, round(quantity, precision))

        elif symbol == "ETHUSDT":
            precision = 3
            quantity = fixed_volume / price
            return max(0.006, round(quantity, precision))

        elif symbol == "DYDXUSDT":
            precision = 1
            quantity = fixed_volume / price
            return max(2.6, round(quantity, precision))

        elif symbol == "APTUSDT":
            precision = 1
            quantity = fixed_volume / price
            return max(0.6, round(quantity, precision))

        elif symbol == "EGLDUSDT":
            precision = 0
            quantity = fixed_volume / price
            return max(0.2, round(quantity, precision))

        elif symbol == "1000PEPEUSDT":
            precision = 0
            quantity = fixed_volume / price
            print("1000pepe")
            return max(336, round(quantity, precision))
        else:
            precision = get_asset_precision(symbol)

        quantity = fixed_volume / price
        print(f"precision {precision} ma[_precision {max_precision}")

        # Ensure precision does not exceed max precision
        if precision > max_precision:
            precision = max_precision

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

async def open_futures_trade(trade_id, symbol, direction):
    try:
        symbol = symbol.upper().replace(" ", "").replace("/", "") + "USDT"
        print(symbol)
        quantity = calculate_quantity(symbol)

        if symbol in ["1000PEPEUSDT", "1000LUNCUSDT"]:
            quantity = round(quantity / 1000, 0)

        print(quantity)
        if contains_keyword(direction, keywords_buy):
            order = client.futures_create_order(
                symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='LONG'
            )
            direction = 'long'
        elif contains_keyword(direction, keywords_sell):
            order = client.futures_create_order(
                symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='SHORT'
            )
            direction = 'short'
        else:
            raise ValueError("Direction must be 'buy' or 'sell'")

        logging.info(f"Trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, "
                     f"Time: {datetime.now()}, Order Details: {order}")

        await save_trade(trade_id, symbol, direction, 'successful_trades.txt')

        redis = await create_redis_connection(db=4)  # Создание подключения к Redis DB 4
        await save_trade_to_redis(redis, trade_id, symbol, direction, cab)

        await open_trade_tg(f"Opened trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, Cab: {cab}")
        return order

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
        #order = await open_futures_trade('12345', 'XRPUSDT', 'buy', 250)  # Пример сделки
        #print(order)
    except Exception as e:
        logging.error(e)
        print(e)

if __name__ == "__main__":
    asyncio.run(main())