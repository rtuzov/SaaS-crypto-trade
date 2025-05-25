# Скрипт для скачивания сигналов из БД
# Работает автоматически, входные данные НЕ принимает

import psycopg2
import sys
import csv
import os
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from datetime import datetime, timedelta

# Параметры подключения к базе данных
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'signals-db',
    'user': 'airflow',
    'password': 'airflow'
}

def delete_data(db_params):
    try:
        # Установка соединения с базой данных
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Вычисление дат
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        print(end_date)
        print(start_date)
        
        # Форматирование дат для SQL запроса
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
        
        print(end_date_str)
        print(start_date_str)
        
        # SQL запрос на удаление
        cursor.execute("""
            DELETE FROM result_db 
            WHERE date >= %s AND date <= %s;
            """, (start_date_str, end_date_str))
        
        # Подтверждение изменений
        conn.commit()
        
        print("Удаление выполнено успешно.")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()

delete_data(db_params)


def fetch_data_to_csv(db_params, file_path):
    try:
        # Установка соединения с базой данных
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # SQL запрос для выборки данных
        cursor.execute("""
            SELECT date, "Symbol", id, direction_gpt, FLOOR(EXTRACT(EPOCH FROM TO_TIMESTAMP(timestamp1, 'YYYY-MM-DD HH24:MI:SS')) * 1000), entryprice
            FROM result_db
            WHERE result LIKE '%No%'
            """)
        
        # Получение данных
        rows = cursor.fetchall()
        
        # Запись данных в CSV файл
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'Symbol', 'id', 'direction_gpt', 'timestamp1', 'entryprice'])
            writer.writerows(rows)
        
        print("Данные успешно сохранены в CSV файл.")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cursor.close()
        conn.close()

# Путь к CSV файлу
csv_file_path = 'result_db_sh.csv'
filename = 'result_db_sh.csv' 
fetch_data_to_csv(db_params, csv_file_path)

