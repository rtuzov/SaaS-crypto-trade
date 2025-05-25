# Скрипт для скачивания сигналов из БД
# Работает автоматически, входные данные НЕ принимает

import psycopg2
import pandas as pd
from datetime import datetime, timedelta

# Параметры подключения к базе данных
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'signals-db',
    'user': 'airflow',
    'password': 'airflow'
}

# SQL запрос
sql_query = """
WITH MarkedRows AS (
    SELECT
        date,
        channel_id,
        message_id,
        crypto_currency_gpt,
        direction_gpt,
        LAG(crypto_currency_gpt, 1) OVER (ORDER BY date, message_id) AS prev_value,
        LEAD(crypto_currency_gpt, 1) OVER (ORDER BY date, message_id) AS next_value
    FROM signals_data
    WHERE (crypto_currency_gpt NOT IN ('НЕ ОПРЕДЕЛЕНО', 'NOT DETERMINED', 'UNKNOWN', 'unknown'))
      AND (direction_gpt NOT IN ('not determined', 'unknown', 'Не определено'))
      AND (CAST(date AS timestamp) BETWEEN %s AND %s)
)
SELECT
    date,
    channel_id,
    message_id,
    crypto_currency_gpt,
    direction_gpt
FROM MarkedRows
WHERE (crypto_currency_gpt != prev_value OR prev_value IS NULL)
   OR (crypto_currency_gpt != next_value AND crypto_currency_gpt = prev_value);
"""

# Вычисляем даты для последних 10 дней
#end_date = (datetime.now() - timedelta(days=3)).date()

end_datetime = (datetime.now() - timedelta(days=0)).date()
end_date = datetime.combine(end_datetime, datetime.max.time())

start_date = end_date - timedelta(days=1)

# Форматирование дат для SQL запроса
start_date_str = start_date.strftime('%Y-%m-%d')
#end_date_str = end_date.strftime('%Y-%m-%d')

end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

try:
    # Подключаемся к базе данных
    with psycopg2.connect(**db_params) as conn:
        # Выполняем запрос
        df = pd.read_sql_query(sql_query, conn, params=(start_date_str, end_date_str))

    # Сохраняем результат в файл
    filename = f"data_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"{filename}")
except Exception as e:
    print("Error:", e)

