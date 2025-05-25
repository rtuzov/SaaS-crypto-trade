import ccxt
import pandas as pd
import time
import telegram
import requests

# Инициализируем клиент Binance
exchange = ccxt.binance({
    'apiKey': 'eGrrQU3E29atX7mPecdinCjVzMQVQu0OckxRBwRnNuQmKB6NJRGdw0ghALSv8cvg',
    'secret': 'TLH1J2kk35L4t0v3aNlnotjsWxxXmmjE0PkQ3qGc1V9suF0Bs9siysKY10SLBkmR',
})

TELEGRAM_BOT_TOKEN = '6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0'
TELEGRAM_CHAT_ID = '-1001998959723'

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# Функция для получения исторических данных
def fetch_ohlcv(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Функция для расчета MACD
def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    df['EMA_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_histogram'] = df['MACD'] - df['Signal_line']
    return df


def detect_anomalies(df, window=20, z_threshold=2.5, delta_threshold=0.5):
    """
    Функция для определения потенциальных и реальных аномалий в гистограмме MACD.
    :param df: DataFrame с данными.
    :param window: Количество периодов для расчета стандартного отклонения.
    :param z_threshold: Пороговое значение Z-счета для определения аномалии.
    :param delta_threshold: Пороговое значение изменений гистограммы MACD для предупреждения о потенциальной аномалии.
    """
    # Расчет стандартного отклонения и среднего для гистограммы MACD
    df['MACD_hist_std'] = df['MACD_histogram'].rolling(window=window).std()
    df['MACD_hist_mean'] = df['MACD_histogram'].rolling(window=window).mean()

    # Расчет Z-счета для каждого значения гистограммы
    df['MACD_hist_z_score'] = (df['MACD_histogram'] - df['MACD_hist_mean']) / df['MACD_hist_std']

    # Расчет дельты (изменения) гистограммы MACD
    df['MACD_histogram_delta'] = df['MACD_histogram'].diff()

    # Определение реальных и потенциальных аномалий
    df['Anomaly'] = df.apply(lambda row: 'Anomaly' if abs(row['MACD_hist_z_score']) > z_threshold else ('Potential' if abs(row['MACD_histogram_delta']) > delta_threshold else 'Normal'), axis=1)

    return df



# Переменная для хранения времени последней аномалии
last_anomaly_time = pd.Timestamp(0)
print("Повторный запуск MACD Anomaly.(with forecast)")
send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "Повторный запуск MACD Anomaly.(with forecast)")
while True:
    try:
        # Получаем данные
        df = fetch_ohlcv('BTC/USDT', '1m', 100)
        # Рассчитываем MACD и ищем аномалии
        df = calculate_macd(df)
        df = detect_anomalies(df)

        # Проверяем наличие новых аномалий
        latest_anomaly = df[df['Anomaly'] == 'Anomaly'].tail(1)

        if not latest_anomaly.empty:
            current_anomaly_time = latest_anomaly['timestamp'].iloc[0]
            if current_anomaly_time > last_anomaly_time:
                print("Найдена новая аномалия:", latest_anomaly[['timestamp', 'MACD_histogram', 'MACD_hist_z_score', 'Anomaly']])
                message = f"Найдена новая аномалия: {latest_anomaly[['timestamp', 'MACD_histogram', 'MACD_hist_z_score', 'Anomaly']].to_string()}"
                send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
                last_anomaly_time = current_anomaly_time

        # Пауза до следующего запроса (60 секунд - время выполнения скрипта)
        time.sleep(60 - time.time() % 60)
    except Exception as e:
        print("Произошла ошибка:", e)
        # Краткая пауза перед повторной попыткой, чтобы избежать бесконечного цикла ошибок
        time.sleep(10)
