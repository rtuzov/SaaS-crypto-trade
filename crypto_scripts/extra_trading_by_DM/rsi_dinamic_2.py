import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

def fetch_binance_data(symbol='BTCUSDT', interval='1m', limit=1):  # Получаем только последнюю минуту данных
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    data = response.json()
    
    columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(data, columns=columns)
    df['Close'] = pd.to_numeric(df['Close'])
    return df

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    loss = delta.where(delta < 0, 0)
    gain = -delta.where(delta > 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def determine_rsi_interval(rsi):
    if rsi > 70:
        return 2  # Сильная перекупленность
    elif 60 < rsi <= 70:
        return 1  # Умеренная перекупленность
    elif 40 <= rsi <= 60:
        return 0  # Нейтральная зона
    elif 30 < rsi < 40:
        return -1  # Умеренная перепроданность
    else:
        return -2  # Сильная перепроданность

def main():
    df_history = pd.DataFrame()  # Исторические данные для расчета RSI
    while True:
        df = fetch_binance_data()
        if not df_history.empty:
            df = pd.concat([df_history, df]).drop_duplicates().tail(500)  # Хранение последних 500 точек данных для расчета RSI
        df['RSI'] = calculate_rsi(df)
        df['RSI Interval'] = df['RSI'].apply(determine_rsi_interval)
        current_row = df[['Close', 'RSI', 'RSI Interval']].iloc[-1]
        print(f"Current Time: {datetime.now()}")
        print(current_row)
        
        df_history = df.copy()
        
        time.sleep(60)  # Пауза на 1 минуту перед следующим запросом

if __name__ == "__main__":
    main()
