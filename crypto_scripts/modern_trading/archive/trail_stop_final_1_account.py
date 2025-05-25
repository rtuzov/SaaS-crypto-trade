from binance.client import Client
import binance.enums as enums
import time
import requests
import telegram
import logging

# Настройка логирования
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Ваши API ключ и секрет
API_KEY = 'eGrrQU3E29atX7mPecdinCjVzMQVQu0OckxRBwRnNuQmKB6NJRGdw0ghALSv8cvg'
API_SECRET = 'TLH1J2kk35L4t0v3aNlnotjsWxxXmmjE0PkQ3qGc1V9suF0Bs9siysKY10SLBkmR'

#Telegram Creds
TELEGRAM_BOT_TOKEN = '6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0'
TELEGRAM_CHAT_ID = '-1001998959723'

# Создание клиента API
client = Client(API_KEY, API_SECRET)

BASE_VALUE = 100  # базовое значение позиции в долларах
INITIAL_STOP_LOSS = -1  # начальный стоп-лосс в долларах
PROFIT_THRESHOLD = 3  # порог прибыли для изменения стоп-лосса
TRAILING_STOP_INCREMENT = (1 - 0.5)  # инкремент для трейлинг стопа

# Словарь для отслеживания стоп-лоссов
stop_loss_dict = {}

def get_open_positions():
    """
    Получение списка всех открытых позиций.
    """
    positions = client.futures_account()['positions']
    return [position for position in positions if float(position['positionAmt']) != 0]

def get_position_key(symbol, is_long):
    """
    Создание уникального ключа для позиции в словаре stop_loss_dict.
    """
    return f"{symbol}_{'LONG' if is_long else 'SHORT'}"


def update_stop_loss(position):
    """
    Обновление стоп-лосса на основе нереализованной прибыли.
    """
    symbol = position['symbol']
    position_amt = float(position['notional'])
    is_long = position_amt > 0
    key = get_position_key(symbol, is_long)
    basis_stop_loss = round(abs(float(position['notional'])) / 100) * INITIAL_STOP_LOSS
    threshold_switch = round(abs(float(position['notional'])) / 100) * PROFIT_THRESHOLD
    increment_switch = round(abs(float(position['notional'])) / 100) * TRAILING_STOP_INCREMENT
    unrealized_profit = float(position['unrealizedProfit'])
    print(position_amt)
    print(basis_stop_loss, threshold_switch, increment_switch)
    position_size = abs(position_amt) * BASE_VALUE

    if key not in stop_loss_dict or unrealized_profit < threshold_switch:
        stop_loss_dict[key] = basis_stop_loss
    else:
        new_stop_loss = unrealized_profit * TRAILING_STOP_INCREMENT
        stop_loss_dict[key] = max(stop_loss_dict[key], new_stop_loss)

def close_position(symbol, quantity, is_long):
    """
    Закрытие позиции с учетом режима хеджирования.
    """
    try:
        # Определение стороны ордера для закрытия позиции
        side = enums.SIDE_SELL if is_long else enums.SIDE_BUY
        position_side = 'LONG' if is_long else 'SHORT'

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=enums.ORDER_TYPE_MARKET,
            quantity=quantity,
            positionSide=position_side
        )
        print("Позиция закрыта", order)

        # Формирование и удаление ключа из словаря стоп-лоссов
        key = get_position_key(symbol, is_long)
        if key in stop_loss_dict:
            del stop_loss_dict[key]

    except Exception as e:
        print(f"Ошибка при закрытии позиции: {e}")


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)


def monitor_and_manage_positions():
    """
    Мониторинг и управление текущими открытыми позициями.
    """
    while True:
        open_positions = get_open_positions()
        for position in open_positions:
            symbol = position['symbol']
            position_amt = float(position['positionAmt'])
            is_long = position_amt > 0
            key = get_position_key(symbol, is_long)
            unrealized_profit = float(position['unrealizedProfit'])

            print(stop_loss_dict)

            update_stop_loss(position)  # Обновление стоп-лосса

            if key in stop_loss_dict:
                stop_loss_value = stop_loss_dict[key]
            else:
                stop_loss_value = INITIAL_STOP_LOSS  # Использование базового стоп-лосса

            #print(f"Symbol: {symbol}, Position: {'LONG' if is_long else 'SHORT'}, Unrealized Profit: {unrealized_profit}, Stop Loss Value: {stop_loss_value}")

            # Логика закрытия позиции
            if (is_long and unrealized_profit <= stop_loss_value) or (not is_long and unrealized_profit <= stop_loss_value):
                close_position(symbol, abs(position_amt), is_long)
                message = f"Закрытие позиции {symbol}, объемом {position_amt} в направлении {'LONG' if is_long else 'SHORT'} с прибылью/убытком {unrealized_profit}"
                logging.info(message)  # Логирование в файл
                send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)

        time.sleep(10)  # Проверка позиций каждые 10 секунд


monitor_and_manage_positions()
