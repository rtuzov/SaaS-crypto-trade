import requests
import pandas as pd
from datetime import datetime
import time
import telegram

# Конфигурация
BINANCE_API_URL = 'https://api.binance.com/api/v3/klines'
TELEGRAM_BOT_TOKEN = '6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0'
TELEGRAM_CHAT_ID = '-1001998959723'
SYMBOL = 'BTCUSDT'
INTERVAL = '5m'
LIMIT = 100


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def fetch_binance_data(symbol, interval, limit):
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(BINANCE_API_URL, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    return df

def calculate_atr(df, period=5):
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['tr0'] = abs(df['High'] - df['Low'])
    df['tr1'] = abs(df['High'] - df['Close'].shift())
    df['tr2'] = abs(df['Low'] - df['Close'].shift())
    tr = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = tr.rolling(period).mean()
    return atr.iloc[-1]

def check_anomaly(df, atr_threshold, volume_threshold):
    current_atr = calculate_atr(df)
    current_volume = float(df.iloc[-1]['Volume'])
    average_volume = df['Volume'].astype(float).mean()
    print(current_atr)
    print(average_volume)
    print(current_volume)
    if current_atr > atr_threshold and current_volume > average_volume * volume_threshold:
        return True
    return False

def main():
    while True:
        df = fetch_binance_data(SYMBOL, INTERVAL, LIMIT)
        if check_anomaly(df, atr_threshold=79, volume_threshold=2.0):  # Thresholds can be adjusted
            print("ANOMALY")
            message = f"Anomaly detected in {SYMBOL}! ATR and Volume thresholds exceeded."
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
        time.sleep(120)  # Check every 2 min

if __name__ == "__main__":
    main()
