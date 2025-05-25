import pandas as pd
from datetime import datetime

# Функция для преобразования даты
from numpy import ndarray
from pandas.core.arrays import ExtensionArray

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import sys
import pandas as pd
'''
# Проверяем, передан ли аргумент
if len(sys.argv) > 1:
    file_path = sys.argv[1]  # Получаем путь к файлу из аргумента командной строки
else:
    raise ValueError("Путь к файлу не был передан")
'''
def convert_date(date_str):
    try:
        # Пытаемся преобразовать дату с учетом дробных секунд
        return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            # Попытка преобразовать дату без дробных секунд
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Если формат все равно не соответствует, возвращаем исходную строку
            return date_str

print('1')
file_path = 'data_test.csv'

with open(file_path, 'r') as file:
    lines = [line.replace('\r', '') for line in file]

# Чтение исходного файла !!!
df = pd.read_csv(file_path, quotechar='"')

# Удаление кавычек и преобразование данных
df['channel_id'] = df['channel_id'].astype(str).str.replace('-', '')
df['id'] = df['channel_id'] + '_' + df['message_id'].astype(str)
df['Symbol'] = df['crypto_currency_gpt']
print(df['date'])
df['date'] = df['date'].apply(convert_date)

# Выбор и переименование колонок
df = df[['date', 'Symbol', 'id', 'direction_gpt']]

# Запись в новый файл
df.to_csv('between_scripts_1.csv', index=False)

# Инициализация сессии для запросов
session = requests.Session()

# Функция для получения цены монеты в конкретный момент времени
def get_price(symbol, timestamp):
    symbol = str(symbol).replace(" ", "").replace("/USDT", "").replace("/", "").replace("1000", "")
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1m&limit=1&endTime={timestamp}"
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            print('good', symbol, float(data[0][4]))
            return float(data[0][4])
    except Exception as e:
        print(f"Ошибка при получении цены для {symbol} на {timestamp}: {str(e)}")
        return None

# Загрузка данных из файла
df = pd.read_csv("between_scripts_1.csv", sep=',')

# Преобразование времени в timestamp с использованием numpy
df['timestamp'] = (pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6).astype(int)

# Функция для обработки строки
def process_row(row):
    timestamp, symbol = row.timestamp, row.Symbol
    price = get_price(symbol, timestamp)
    return price

# Использование ThreadPoolExecutor для параллельной обработки строк
with ThreadPoolExecutor(max_workers=10) as executor:
    df['entryprice'] = list(executor.map(process_row, df.itertuples(index=False)))

#Удаление строк с пустым значением в колонке entry_price
df = df.dropna(subset=["entryprice"])

# Сохранение измененного DataFrame в файл
df.to_csv("between_scripts_1_Modified.csv", index=False)

#СЕКЦИЯ ОБРАБОТКИ НАПРАВЛЕНИЙ
# Функция для чтения классификаций из файла
def read_classifications(file_path):
    df = pd.read_csv(file_path)
    return df['long_values'].dropna().tolist(), df['short_values'].dropna().tolist(), df['undefined_values'].dropna().tolist()

# Функция для обработки данных
def process_trading_data(input_file_path, output_file_path, undefined_values_file_path, classifications_file_path):
    # Чтение классификаций из файла
    long_values, short_values, undefined_values = read_classifications(classifications_file_path)

    # Загрузка данных из файла
    data = pd.read_csv(input_file_path)

    # Колонка с направлениями сделок
    direction_column = 'direction_gpt'

    # Функция для преобразования значения направления сделки
    def transform_direction(direction):
        print(direction)
        # Нормализация строки
        normalized_direction = str(direction).strip().lower()

        #МЕСТО ГДЕ МЕНЯЕТСЯ РЕВЕРС
        # Преобразование в "long" или "short"
        if any(lng in normalized_direction for lng in long_values):
            return 'long'
        elif any(srt in normalized_direction for srt in short_values):
            return 'short'
        else:
            return 'undefined'

    # Преобразование направлений сделок
    data['transformed_direction'] = data[direction_column].apply(transform_direction)

    # Сохранение изменённых данных
    data.to_csv(output_file_path, index=False)

    # Сохранение неопределённых значений
    undefined_data = data[data['transformed_direction'] == 'undefined']
    undefined_data.to_csv(undefined_values_file_path, index=False)

    print(f"Data processed and saved to {output_file_path}. Undefined values saved to {undefined_values_file_path}.")

#ПРЕДФИНАЛЬНАЯ ОБРАБОТКА КОЛОНОК
def process_file(input_file_path, output_file_path):
    # Чтение данных из файла
    data = pd.read_csv(input_file_path)

    # Удаление строк, где последняя колонка содержит 'undefined'
    data = data[data.iloc[:, -1] != 'undefined']

    # Поменять местами колонки 'direction_gpt' и 'transformed_direction'
    columns = list(data.columns)
    dir_idx, trans_idx = columns.index('direction_gpt'), columns.index('transformed_direction')
    columns[dir_idx], columns[trans_idx] = columns[trans_idx], columns[dir_idx]
    data = data[columns]

    # Удаление последней колонки
    data = data.iloc[:, :-1]

    # Переименование колонки 'transformed_direction' в 'direction_gpt'
    data.rename(columns={'transformed_direction': 'direction_gpt', 'timestamp': 'timestamp1'}, inplace=True)

    # Сохранение обработанных данных в файл
    data.to_csv(output_file_path, index=False)


# Пути к файлам (указывайте свои пути здесь)
input_file_path = 'between_scripts_1_Modified.csv'  # Исходный файл с данными
output_file_path = 'between_scripts_1_Modified_FINAL.csv'  # Файл для сохранения изменённых данных
undefined_values_file_path = 'between_scripts_1_Modified_undefined_values.csv'  # Файл для неопределённых значений
classifications_file_path = 'trading_directions_classification.csv'  # Файл со словарём классификаций

# Вызов функции для обработки данных
process_trading_data(input_file_path, output_file_path, undefined_values_file_path, classifications_file_path)

# Пути к файлам для ПРЕДФИНАЛЬНОЙ ОБРАБОТКИ
input_file_path = output_file_path  # Укажите путь к исходному файлу
output_file_path = 'FINAL' + output_file_path  # Укажите путь к выходному файлу

# Вызов функции для обработки файла
process_file(input_file_path, output_file_path)

# Удаление ненужных промежуточных файлов
os.remove('between_scripts_1.csv')
os.remove('between_scripts_1_Modified.csv')
os.remove('between_scripts_1_Modified_FINAL.csv')
