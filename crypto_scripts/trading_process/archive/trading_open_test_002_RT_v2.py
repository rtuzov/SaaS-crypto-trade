from binance.client import Client
import binance.enums as enums
import math
import csv
import time
from datetime import datetime

RISK_AMOUNT = 100

#Daniil
#api_key = 'fjvtCG1OezpVyk7c8INny1iGji376QOEtRQcQxFjDoFjiAVTpCsRe1MgmBFDOCNm'
#api_secret = 'FQC5Io9MG8T6YrwDXLH0vRLE1NdJfvLoq1xUAgOVcWLZpQEEWeCKvhskSb8pfWIz'

#Subaccount_credentials
api_key = '4y4Cn7UewXQhhF5ioN0xQVDiGkTiFqlLfqt5Au3AgkikfhkaY4MZIkcbpRAPKKSa'
api_secret = 'LmpyW7a4JWPr8Ik50wTtwRS8aBReV7U8h1H5EDiXcTftTiNz28sKqDmd0Ea8kfA8'

#Roma
api_key_2 = 'zKDSXzPBAQKjle8mA3HfnG6y0BJTBTYK7A4IxDHXLPoJNQGCoN09ItB6mbWWYjyR'
api_secret_2 = 'r7VQzJTovajtwY5UJUxb3PK3iNGDFIuGSF8ISWjwbGhcZYiCpF1dwnllexYPF2pH'


client = Client(api_key, api_secret)
client_2 = Client(api_key_2, api_secret_2)

def log_trade(log_file, symbol, direction, status):
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), symbol, direction, status])

def get_current_price(symbol):
    """
    Получение текущей цены для заданной монеты.
    :param symbol: Символ монеты (например, 'BTCUSDT').
    :return: Текущая цена.
    """
    ticker = client.get_ticker(symbol=symbol)
    print('INSIDE CCURRENT PRICE', ticker)
    return float(ticker['lastPrice'])

def calculate_position_size(current_price, risk_amount, step_size):
    """
    Расчет размера позиции на основе риска и текущей цены.
    :param current_price: Текущая цена монеты.
    :param risk_amount: Фиксированный риск в долларах.
    :param step_size: Шаг размера позиции.
    :return: Размер позиции в монетах.
    """
    position_size = risk_amount / current_price
    something_cool = math.floor(position_size / step_size) * step_size
    print('INSIDE POSITION SIZE', position_size, something_cool)
    return math.floor(position_size / step_size) * step_size

def open_futures_position2(symbol, direction, risk_amount = RISK_AMOUNT):
    """
    Открытие позиции на фьючерсном рынке.
    :param symbol: Символ монеты.
    :param direction: Направление ('buy' или 'sell').
    :param risk_amount: Фиксированный риск в долларах.
    """
    try:
        symbol = symbol.replace(" ", "")
        symbol = symbol.replace("/", "")

        # Добавление 'USDT' к символу, если необходимо
        if not symbol.endswith("USDT"):
            symbol += "USDT"
            symbol = symbol.replace(" ", "")

        #This is Symbol for info purpose Delete after debug
        print("Inside open_futures", symbol)

        symbol_info = client.futures_exchange_info()['symbols']
        step_size = next((float(info['filters'][2]['stepSize']) for info in symbol_info if info['symbol'] == symbol), 0.01)

        current_price = get_current_price(symbol)
        position_size = calculate_position_size(current_price, risk_amount, step_size)

        #This is Symbol for info purpose Delete after debug
        #print("Inside open_futures", symbol)

        side=enums.SIDE_BUY if direction.lower() == 'long/buy/покупка' else enums.SIDE_SELL

        #Daniil's order open
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=enums.ORDER_TYPE_MARKET,
                quantity=position_size
            )
            print(order)
            log_trade("Daniil_logs.csv", symbol, direction, "OK")
        except Exception as e:
            print(f"Daniil's order error: {e}")
            log_trade("Daniil_logs.csv", symbol, direction, "DENIED")

        #Roma order open
        #order_2 = client_2.futures_create_order(
         #   symbol=symbol,
          #  side=side,
           # type=enums.ORDER_TYPE_MARKET,
            #quantity=position_size
        #)
        #print(order_2)
        return order
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

