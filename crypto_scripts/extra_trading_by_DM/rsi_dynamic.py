import requests
import pandas as pd
import time
from datetime import datetime

def fetch_binance_data(symbol='BTCUSDT', interval='1m', limit=500):
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    data = response.json()
    
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(data, columns=columns)
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    
    return df

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()[:window+1]
    avg_loss = loss.rolling(window=window, min_periods=window).mean()[:window+1]

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def main():
    while True:
        df = fetch_binance_data()
        df['RSI'] = calculate_rsi(df)
        print(f"Current Time: {datetime.now()}")
        print(df[['Close', 'RSI']].tail(1))
        
        # Ждём минуту до следующего обновления
        time.sleep(60)

# Запускаем основную функцию
if __name__ == "__main__":
    main()
