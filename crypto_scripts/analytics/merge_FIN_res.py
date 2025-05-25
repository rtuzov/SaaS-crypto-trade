import pandas as pd

# Загрузка данных из первого файла
df1 = pd.read_csv('FINALbetween_scripts_1_Modified_FINAL.csv')

# Загрузка данных из второго файла, пропускаем первую строку (шапку)
df2 = pd.read_csv('result_db_sh.csv', skiprows=1)

# Убедимся, что колонки второго датафрейма соответствуют первому
df2.columns = df1.columns

# Добавление данных из второго файла в первый
combined_df = pd.concat([df1, df2], ignore_index=True)

# Сохранение результата в новый CSV файл
combined_df.to_csv('FINALbetween_scripts_1_Modified_FINAL_combined_result.csv', index=False)
