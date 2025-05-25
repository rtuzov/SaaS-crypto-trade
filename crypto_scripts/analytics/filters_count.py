import pandas as pd
import csv
from datetime import datetime, timedelta
import sys
import os

# Функция для создания диапазона дат
def create_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_range = [start + timedelta(days=x) for x in range(0, (end-start).days + 1)]
    return [date.strftime("%Y-%m-%d") for date in date_range]

def load_and_process_data(file_path, date):
    """
    Функция для первичной обработки данных.
    """
    df = pd.read_csv(file_path)
    df[['channel_id', 'message_id']] = df['id'].str.split('_', expand=True)

    result_conditions = {
        'No data after signal': 'No data after signal',
        'No TP/SL Hit': 'No TP/SL Hit',
        'SL Hit': 'SL Hit',
        'TP 3% Hit': 'TP 3% Hit',
        'TP 4% Hit': 'TP 4% Hit',
        'TP 5% Hit': 'TP 5% Hit'
    }

    for new_column, result_value in result_conditions.items():
        df[new_column] = df['result'].apply(lambda x: 1 if x == result_value else 0)

    output_file = f'./strategy1/strategy1_{date}.csv'
    df.to_csv(output_file, index=False)
    print(f"Файл сохранен как: {output_file}")

    return output_file

def summarize_data(file_path, start_date, days_back):
    """
    Функция для подсчета итоговых показателей с фильтрацией по временному диапазону.
    """
    df = pd.read_csv(file_path)
    start_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=0)
    end_date = start_date - timedelta(days=days_back)
    
    print(start_date)
    print(end_date)

    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= end_date) & (df['date'] <= start_date)]

    print(df)
    df['TP_final'] = df['TP 3% Hit'] + df['TP 4% Hit'] + df['TP 5% Hit']
    df['work_signals'] = df['TP 3% Hit'] + df['TP 4% Hit'] + df['TP 5% Hit'] + df['SL Hit']

    summary = df.groupby('channel_id').agg({
        'TP_final': 'sum',
        'work_signals': 'sum',
        'No data after signal': 'sum',
        'No TP/SL Hit': 'sum',
        'SL Hit': 'sum',
        'TP 3% Hit': 'sum',
        'TP 4% Hit': 'sum',
        'TP 5% Hit': 'sum',
        'channel_id': 'count'
    }).rename(columns={'channel_id': 'all_signals'})

    summary['winrate'] = summary['TP_final'] / summary['work_signals']
    summary.to_csv('./strategy1/strategy1_tech.csv')

def filter_data(quantity, winrate_setup):
    """
    Функция для фильтрации данных на основе установленных условий и временного диапазона.
    """
    filtered_channel_ids = []
    with open('./strategy1/strategy1_tech.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                work_signals = int(row['work_signals'])
                winrate = float(row['winrate']) if row['winrate'] else 0.0
            except ValueError:
                continue

            if work_signals > quantity and winrate > winrate_setup:
                filtered_channel_ids.append(row['channel_id'])

    with open('./strategy1/filter.txt', 'w') as file:
        for channel_id in filtered_channel_ids:
            file.write(f"{channel_id}\n")

    return filtered_channel_ids

def process_data_with_tag(file_path, start_date, days_back, filtered_channel_ids):
    """
    Функция для обработки данных с добавлением тегов.
    """
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date']).dt.date

    next_day = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1)
    df = df[df['date'] == next_day.date()]

    if df.empty:
        print(f"Нет данных для даты: {next_day.date()}")
    else:
        filtered_channel_ids = [int(x) for x in filtered_channel_ids if x.isdigit()]
        df['tag1'] = df['channel_id'].apply(lambda x: 1 if x in filtered_channel_ids else 0)

        df_tag1 = df[df['tag1'] == 1]

        TP_last = df_tag1[['TP 3% Hit', 'TP 4% Hit', 'TP 5% Hit']].sum().sum()
        All_last = df_tag1[['TP 3% Hit', 'TP 4% Hit', 'TP 5% Hit', 'SL Hit']].sum().sum()

        winrate_last = (TP_last / All_last) * 100 if All_last > 0 else 0

        output_file = f"{next_day.strftime('%Y-%m-%d')}_{days_back}.csv"
        df_tag1.to_csv(output_file, index=False)
        print(f"Файл сохранен как: {output_file}")

        return [next_day.strftime('%Y-%m-%d'), winrate_last, TP_last, All_last, days_back, len(filtered_channel_ids)]

def main():
    file_path = 'analytics_filter.csv'
    current_date = datetime.now()
    end_date = current_date.strftime('%Y-%m-%d')
    start_date = (current_date - timedelta(days=0)).strftime('%Y-%m-%d')
    
    days_back_options = [60]

    # Получение абсолютного пути к родительской директории
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Добавление родительской директории в sys.path
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        from config import quantity1, winrate_setup1, days_back_options1
        if isinstance(days_back_options1, int):
            days_back_options = [days_back_options1]
        else:
            days_back_options = days_back_options1
    except ImportError as e:
        print(f"Ошибка при импорте модуля config: {e}")
        sys.exit(1)

    date_range = create_date_range(start_date, end_date)
    results = []
    print(date_range, results)
    
    print(f"days_back_options {days_back_options} {quantity1} {winrate_setup1}")
	
    for date in date_range:
        print(file_path, date)
        processed_file = load_and_process_data(file_path, date)
        for days_back in days_back_options: 	
        
            print(processed_file ,date, days_back)
            summarize_data(processed_file, date, days_back)
            print(quantity1, winrate_setup1)
            filtered_channel_ids = filter_data(quantity1, winrate_setup1)
            #result = process_data_with_tag(processed_file, date, days_back, filtered_channel_ids)
            #if result:
            #    results.append(result)

    results_df = pd.DataFrame(results, columns=['start_date', 'winrate_last', 'tp_last', 'all_last', 'days_back_options', 'filtered_channels_count'])
    results_df.to_csv('./strategy1/final_results3.csv', index=False)

if __name__ == "__main__":
    main()
