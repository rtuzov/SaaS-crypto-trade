import pandas as pd
import psycopg2
from psycopg2 import extras

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

# Чтение данных из CSV
def read_data_from_csv(file_path):
    return pd.read_csv(file_path)

# Обновление или вставка данных в базу данных
def upsert_data(connection, data):
    cursor = connection.cursor()
    # Подготовим шаблоны SQL для вставки и обновления
    insert_query = """
        INSERT INTO result_db (coin_type, date, "Symbol", id, direction_gpt, timestamp1, entryprice,
                                timestamp1_rounded, "TP_2", "TP_3", "TP_4", "SL", result, result_time, delta_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    update_query = """
        UPDATE result_db SET 
            coin_type = %s, date = %s, "Symbol" = %s, direction_gpt = %s, timestamp1 = %s, entryprice = %s,
            timestamp1_rounded = %s, "TP_2" = %s, "TP_3" = %s, "TP_4" = %s, "SL" = %s, "result" = %s, "result_time" = %s, "delta_time" = %s 
        WHERE id = %s;
    """
    # Проверка и обновление или вставка
    for index, row in data.iterrows():
        cursor.execute("SELECT id FROM result_db WHERE id = %s;", (row['id'],))
        result = cursor.fetchone()
        if result is not None:
            # Обновить существующую запись
            cursor.execute(update_query, (row['coin_type'], row['date'], row['Symbol'], row['direction_gpt'],
                                          row['timestamp1'], row['entryprice'], row['timestamp1_rounded'],
                                          row['TP_2'], row['TP_3'], row['TP_4'], row['SL'], row['result'],
                                          row['result_time'], row['delta_time'], row['id']))
        else:
            # Вставить новую запись
            cursor.execute(insert_query, (row['coin_type'], row['date'], row['Symbol'], row['id'],
                                          row['direction_gpt'], row['timestamp1'], row['entryprice'],
                                          row['timestamp1_rounded'], row['TP_2'], row['TP_3'], row['TP_4'],
                                          row['SL'], row['result'], row['result_time'], row['delta_time']))
    connection.commit()
    cursor.close()

# Основная функция
def main():
    connection = connect_to_db(db_params)
    data = read_data_from_csv('result/analytics_day.csv')
    upsert_data(connection, data)
    connection.close()

if __name__ == "__main__":
    main()
