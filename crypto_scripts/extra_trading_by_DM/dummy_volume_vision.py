import ccxt
import pandas as pd
import time
import telegram
import requests

TELEGRAM_BOT_TOKEN = '6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0'
TELEGRAM_CHAT_ID = '-1001998959723'

# Подключение к Binance
exchange = ccxt.binance()

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# Функция для получения исторических данных
def fetch_ohlcv(symbol, timeframe='5m', limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


# Функция для определения аномалий
def detect_anomalies(df):
    df['Anomaly'] = False
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i - 1]
        if ((current_row['high'] > previous_row['high'] or current_row['low'] < previous_row['low']) and
                current_row['volume'] > 2 * previous_row['volume']):
            df.at[current_row.name, 'Anomaly'] = True
    return df


symbol = 'BTC/USDT'
timeframe = '5m'
limit = 2  # Достаточно анализировать последние две свечи

while True:
    try:
        # Получаем данные
        df = fetch_ohlcv(symbol, timeframe, limit)

        # Определяем аномалии
        df = detect_anomalies(df)

        # Выводим аномалии, если они есть
        anomalies = df[df['Anomaly'] == True]
        #print(df)
        if not anomalies.empty:
            print("Найдена аномалия:", anomalies[['open', 'high', 'low', 'close', 'volume', 'Anomaly']])
            message = f"Найдена новая аномалия по объему ⤴️ : {anomalies[['open', 'high', 'low', 'close', 'volume', 'Anomaly']].to_string()}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)


        # Пауза на 5 минут до следующей проверки
        time.sleep(60)  # Пауза в 300 секунд (5 минут)
    except Exception as e:
        print("Произошла ошибка:", e)
        # Краткая пауза перед следующей попыткой, чтобы избежать бесконечного цикла ошибок
        time.sleep(60)
