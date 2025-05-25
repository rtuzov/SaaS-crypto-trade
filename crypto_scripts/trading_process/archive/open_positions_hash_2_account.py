from binance.client import Client
from binance.enums import *
import logging
from datetime import datetime
import asyncio

"""
Как использовать?
order = open_futures_trade('12345', 'XRPUSDT', 'buy', 250)
Данные должны передваться в эту фунцию вместе а айди сделки в виде айди канала + сообщения.
Размер позы тоже передается в зависимости от акка

Логи пишутся в один файл
Можно идентифицировать счета по размеру позы
"""

FIXED_VOLUME = 100

# Настройка логирования
logging.basicConfig(filename='futures_trades_account_2.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Параметры API
#api_key = 'eGrrQU3E29atX7mPecdinCjVzMQVQu0OckxRBwRnNuQmKB6NJRGdw0ghALSv8cvg'
#api_secret = "TLH1J2kk35L4t0v3aNlnotjsWxxXmmjE0PkQ3qGc1V9suF0Bs9siysKY10SLBkmR"
api_key_2 = "UdHx4OzSs3by5FK0T6rMQZi1FE3pNV1mVwPUvW1ZDJAfUVLb2cuJnWUV3j3AeuJC"
api_secret_2 = 'BeLZPDpkDRxRv2KLfrRKbEokQny5WTsJmSpl5Z1Ei5YsduUarhjgKVXR2Z6qFA5V'
#api_key_3 = "fjvtCG1OezpVyk7c8INny1iGji376QOEtRQcQxFjDoFjiAVTpCsRe1MgmBFDOCNm"
#api_secret_3 = 'FQC5Io9MG8T6YrwDXLH0vRLE1NdJfvLoq1xUAgOVcWLZpQEEWeCKvhskSb8pfWIz'
#api_key_4 = "fjvtCG1OezpVyk7c8INny1iGji376QOEtRQcQxFjDoFjiAVTpCsRe1MgmBFDOCNm"
#api_secret_4 = 'FQC5Io9MG8T6YrwDXLH0vRLE1NdJfvLoq1xUAgOVcWLZpQEEWeCKvhskSb8pfWIz'

# Создание клиента API для работы с USDⓈ-M фьючерсами
client = Client(api_key_2, api_secret_2)

# Функция для получения точности количества для актива
def get_asset_precision(symbol):
    info = client.get_symbol_info(symbol)
    for filter in info['filters']:
        if filter['filterType'] == 'LOT_SIZE':
            return filter['stepSize'].find('1') - 1
    return -1  # Возвращает -1 в случае, если информация не найдена

# Измененная функция для расчета количества с учетом точности
def calculate_quantity(symbol, fixed_volume):
    price = client.get_symbol_ticker(symbol=symbol)['price']
    precision = get_asset_precision(symbol)
    quantity = fixed_volume / float(price)
    return round(quantity, precision)

# Функция для открытия фьючерсной сделки
def open_futures_trade_second(trade_id, symbol, direction, fixed_volume = FIXED_VOLUME):
    print("______SYMBOL_____", symbol)
    print(trade_id, symbol, direction, fixed_volume)
    # Добавление 'USDT' к символу, если необходимо
    symbol += "USDT"
    symbol = symbol.replace(" ", "")
    symbol = symbol.replace(" ", "")
    symbol = symbol.replace("/", "")
    print("EXTRA_NEEW", symbol)
    quantity = calculate_quantity(symbol, fixed_volume)
    print("NEW SYMBOL",symbol)

    if direction.lower() == 'long/buy/покупка':
        order = client.futures_create_order(symbol=symbol, side=SIDE_BUY,
                                            type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='LONG')
        order = client.futures_create_order(symbol=symbol, side=SIDE_SELL,
                                            type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='SHORT')
    elif direction.lower() == 'short/sell/продажа':
        order = client.futures_create_order(symbol=symbol, side=SIDE_SELL,
                                            type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='SHORT')
        order = client.futures_create_order(symbol=symbol, side=SIDE_BUY,
                                            type=ORDER_TYPE_MARKET, quantity=quantity, positionSide='LONG')
    else:
        raise ValueError("Direction must be 'buy' or 'sell'")

    logging.info(f"Trade ID: {trade_id}, Symbol: {symbol}, Direction: {direction}, "
                 f"Time: {datetime.now()}, Order Details: {order}")
    return order

# Пример использования
try:
    #response = client.futures_change_position_mode(dualSidePosition=True)
    #print(response)
    current_mode = client.futures_get_position_mode()
    print(current_mode)
    #order = open_futures_trade('12345', 'XRPUSDT', 'buy', 250)  # Пример сделки
    print(order)
except Exception as e:
    logging.error(e)
    print(e)
