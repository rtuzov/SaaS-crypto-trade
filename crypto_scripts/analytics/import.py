import csv
import psycopg2
from psycopg2 import sql

# Параметры подключения к базе данных
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'signals-db',
    'user': 'airflow',
    'password': 'airflow'
}

# Функция для создания соединения с базой данных
def connect_db(params):
    conn = psycopg2.connect(
        host=params['host'],
        port=params['port'],
        dbname=params['database'],
        user=params['user'],
        password=params['password']
    )
    conn.autocommit = True
    return conn

# Функция для загрузки данных из CSV в таблицу result_db
def load_data_from_csv(file_path):
    conn = connect_db(db_params)
    cursor = conn.cursor()

    # Открываем CSV файл
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Читаем заголовки для определения столбцов

        # Создаем таблицу, если она еще не существует
        cursor.execute(
            sql.SQL("DROP TABLE IF EXISTS result_db;")
        )
        cursor.execute(
            sql.SQL("CREATE TABLE result_db ({})").format(
                sql.SQL(', ').join(sql.SQL("{} TEXT").format(sql.Identifier(h)) for h in headers)
            )
        )
        
        # Подготавливаем SQL запрос для вставки данных
        insert_query = sql.SQL("INSERT INTO result_db ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, headers)),
            sql.SQL(', ').join(sql.Placeholder() * len(headers))
        )

        # Вставляем данные
        for row in reader:
            cursor.execute(insert_query, row)
    
    cursor.close()
    conn.close()

# Путь к CSV файлу
csv_file_path = 'result1.csv'

# Вызываем функцию для загрузки данных
load_data_from_csv(csv_file_path)
