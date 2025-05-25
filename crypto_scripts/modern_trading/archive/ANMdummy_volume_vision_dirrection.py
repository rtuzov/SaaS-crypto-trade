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

def write_anomaly_signal(signal_type):
    with open("anomaly_signal.txt", "w") as file:
        file.write(signal_type)

# Модифицируем функцию для записи аномалий в файл
def write_anomaly_logs(signal_type, anomalies):
    with open("anomaly_signal_logs.txt", "a") as file:  # Изменяем режим на "a" для добавления данных
        for index, row in anomalies.iterrows():
            file.write(f"{index}, {row['open']}, {row['high']}, {row['low']}, {row['close']}, {row['volume']}, {signal_type}\n")

# В месте обнаружения аномалии вызываем функцию
# Например, write_anomaly_signal("LONG") для аномалии лонг


# Функция для определения аномалий
def detect_anomalies(df):
    df['Market_Trend'] = df['close'].diff().apply(lambda x: 'Up' if x > 0 else 'Down')
    df['Candle_Type'] = (df['close'] > df['open']).apply(lambda x: 'LONG' if x else 'SHORT')
    df['Anomaly'] = False
    df['Anomaly_Type'] = None
    
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i-1]
        
        if ((current_row['high'] > previous_row['high'] or current_row['low'] < previous_row['low']) and
            current_row['volume'] > 2 * previous_row['volume']):
            df.at[current_row.name, 'Anomaly'] = True
            
            # Определение типа аномалии
            if current_row['Market_Trend'] == 'Up' and current_row['Candle_Type'] == 'LONG':
                anomaly_type = 'Up_Long'
            elif current_row['Market_Trend'] == 'Up' and current_row['Candle_Type'] == 'SHORT':
                anomaly_type = 'Up_Short'
            elif current_row['Market_Trend'] == 'Down' and current_row['Candle_Type'] == 'LONG':
                anomaly_type = 'Down_Long'
            else: # Down and Short
                anomaly_type = 'Down_Short'
                
            df.at[current_row.name, 'Anomaly_Type'] = anomaly_type

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
        print(df)
        print("THIS Is candle", df['Candle_Type'].tolist())

        if not anomalies.empty:
            candle_type = df['Candle_Type'].tolist()
            candle_type_final = candle_type[0]
            #write_anomaly_logs(candle_type_final, anomalies)
            print("Найдена аномалия:", anomalies[['open', 'high', 'low', 'close', 'volume', 'Anomaly']])
            message = f"Найдена новая аномалия по объему ⤴️  и с НАПРАЛЕНИЕМ: {anomalies[['open', 'close', 'volume', 'Market_Trend', 'Candle_Type', 'Anomaly', 'Anomaly_Type']].to_string()}"
            for index, row in anomalies.iterrows():
                message_2 = f"{row['Candle_Type']}\n"
            print("this is message 3", message_2)
            write_anomaly_logs(message_2, anomalies)
            write_anomaly_signal(message_2)
            message_3 = f"То что пойдет в функцию с закрытием позы⤴️  и с НАПРАЛЕНИЕМ: {message_2}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message_3)


        # Пауза на 5 минут до следующей проверки
        time.sleep(60)  # Пауза в 300 секунд (5 минут)
    except Exception as e:
        print("Произошла ошибка:", e)
        # Краткая пауза перед следующей попыткой, чтобы избежать бесконечного цикла ошибок
        time.sleep(60)
