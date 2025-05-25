import os
import pandas as pd

def combine_csv_files(folder_path):
    # Папка с CSV файлами
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # Список для хранения содержимого всех файлов
    data_frames = []
    
    for file in files:
        # Полный путь к файлу
        full_file_path = os.path.join(folder_path, file)
        
        # Чтение CSV файла
        df = pd.read_csv(full_file_path)
        
        # Замена ".0" на пустое значение в столбце 'id'
        df['id'] = df['id'].astype(str).str.replace('.0', '')
        
        # Добавление DataFrame в список
        data_frames.append(df)
    
    # Объединение всех DataFrame в один
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    # Удаление дубликатов шапки, если они есть
    combined_df = combined_df.drop_duplicates()
    
    # Сортировка по дате
    combined_df = combined_df.sort_values('date')
    
    # Запись в файл
    combined_df.to_csv('result1.csv', index=False)

# Укажите путь к папке с файлами
folder_path = 'result'
combine_csv_files(folder_path)
