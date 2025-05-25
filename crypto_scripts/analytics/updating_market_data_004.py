import requests
import pandas as pd
from datetime import datetime
import os

# Путь к папке с вашими файлами
directory = '/root/my_test/fully_automated_analytics/new_coin_data'
error_file = '/root/my_test/fully_automated_analytics/error_data_update.csv'

base_url = 'https://fapi.binance.com/fapi/v1/klines'
interval = '5m'

# Обрабатываем каждый файл в директории
for file_name in os.listdir(directory):
    print(file_name)
    if file_name.endswith('_data.csv'):
        #base_currency = ''.join([i for i in file_name if not i.isdigit()]).replace('data.csv', '').replace('USDT', '').replace('BUSD', '').replace('_', '')
        base_currency = file_name.split("USDT")[0].replace("_data.csv", "")
        print(base_currency)
        for quote_currency in ['USDT', 'BUSD']:
            symbol = base_currency + quote_currency
            print(symbol)
            file_path = os.path.join(directory, file_name)
            print("this is FILEPATH", file_path)

            # Получаем последнюю дату из файла
            try:
                df = pd.read_csv(file_path)
                last_date_str = df.iloc[-1]['timestamp']
                last_date = datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')
                start_time = int(last_date.timestamp() * 1000)
            except Exception as e:
                start_time = int((datetime.now() - pd.Timedelta(days=1)).timestamp() * 1000)

            params = {
                'symbol': symbol,
                'interval': interval,
                'startTime': start_time,
                'limit': 1000  # Максимальное количество записей за один запрос
            }

            ohlcv = []
            while True:
                response = requests.get(base_url, params=params)
                data = response.json()
                if not data or 'code' in data:
                    break  # Выход, если нет данных или ошибка
                ohlcv.extend(data)
                last_candle = data[-1]
                params['startTime'] = last_candle[0] + 5 * 60000  # Следующий интервал

            # Преобразование данных и добавление к файлу
            if ohlcv:
                new_data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
                new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], unit='ms')
                print("_______----------_______")
                df = pd.concat([df, new_data])
                df.to_csv(file_path, index=False)

print("Данные обновлены.")
