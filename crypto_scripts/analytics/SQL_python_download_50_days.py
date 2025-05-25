import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

# Параметры подключения к базе данных
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'signals-db',
    'user': 'airflow',
    'password': 'airflow'
}

# Функция для подключения к базе данных
def connect_to_db(params):
    connection = psycopg2.connect(**params)
    return connection

# Функция для загрузки данных из базы в CSV
def export_data_to_csv(connection):
    cursor = connection.cursor()
    # Рассчитаем дату 50 дней назад от текущего момента
    fifty_days_ago = datetime.now() - timedelta(days=50)
    # Формируем запрос для выборки данных за последние 50 дней
    query = sql.SQL("""
        SELECT * FROM result_db
        WHERE date::timestamp >= %s;
    """)
    # Выполнение запроса
    cursor.execute(query, [fifty_days_ago])
    # Получение результатов запроса
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    # Закрытие курсора
    cursor.close()
    # Сохранение данных в CSV
    df.to_csv('analytics_filter.csv', index=False)

# Основная функция
def main():
    connection = connect_to_db(db_params)
    export_data_to_csv(connection)
    connection.close()

if __name__ == "__main__":
    main()
