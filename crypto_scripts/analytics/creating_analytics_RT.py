import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import sys
from datetime import datetime


import os, shutil
if not os.path.exists('coin_results'):
    os.makedirs('coin_results')

# Импорт библиотек R
base = importr('base')
dplyr = importr('dplyr')

# Чтение даты из аргументов командной строки и конвертация в datetime
date_str = sys.argv[1]
analysis_date = datetime.strptime(date_str, '%Y-%m-%d')

# Конвертация объекта datetime обратно в строку для R
analysis_date_str = analysis_date.strftime('%Y-%m-%d')

# Загрузка R скрипта
robjects.r.source('/root/my_test/fully_automated_analytics/r_VM_version_RT_v1.r')

# Путь к файлу данных
signals_data_path = '/root/my_test/fully_automated_analytics/FINALbetween_scripts_1_Modified_FINAL.csv'

print("Using file path:", signals_data_path)

# Вызов функции run_entire_script из вашего R скрипта
robjects.r['run_entire_script'](signals_data_path, analysis_date_str)

print('File 1 - ready')

# Путь к файлу данных 2
#signals_data_path2 = '/root/my_test/fully_automated_analytics/FINALbetween_scripts_1_Modified_FINAL_2.csv'

# Загрузка и выполнение второго R скрипта
#robjects.r.source('/root/my_test/fully_automated_analytics/r_VM_version_RT_v2.r')
#robjects.r['run_entire_script'](signals_data_path2)

#print('File 2 - ready')

# Путь к файлу данных 3
#signals_data_path3 = '/root/my_test/fully_automated_analytics/FINALbetween_scripts_1_Modified_FINAL_3.csv'

# Загрузка и выполнение второго R скрипта
#robjects.r.source('/root/my_test/fully_automated_analytics/r_VM_version_RT_v3.r')
#robjects.r['run_entire_script'](signals_data_path3)

#print('File 3 - ready')

# Путь к файлу данных 4
#signals_data_path4 = '/root/my_test/fully_automated_analytics/FINALbetween_scripts_1_Modified_FINAL_4.csv'

# Загрузка и выполнение второго R скрипта
#robjects.r.source('/root/my_test/fully_automated_analytics/r_VM_version_RT_v4.r')
#robjects.r['run_entire_script'](signals_data_path4)


#print('File 4 - ready')

# Теперь весь ваш R скрипт выполнится с указанным путем к файлу

if os.path.isdir("coin_results"):
    shutil.rmtree("coin_results")
#Раскоментить когда скачает Рома
#os.remove("FINALbetween_scripts_1_Modified_FINAL.csv")
