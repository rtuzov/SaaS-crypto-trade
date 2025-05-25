import subprocess
import requests
import shutil
import os
import pandas as pd  


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)
    
def split_csv_file(filename, lines_per_file=18000):
    # Чтение файла с помощью pandas для сохранения заголовков
    df = pd.read_csv(filename)
    # Определение количества файлов на основе размера датафрейма
    num_files = len(df) // lines_per_file + (1 if len(df) % lines_per_file else 0)
    
    for i in range(num_files):
        start = i * lines_per_file
        end = start + lines_per_file
        # Создание нового датафрейма для каждого файла
        df_subset = df.iloc[start:end]
        # Сохранение файла с добавлением суффикса к имени
        new_filename = f"{filename.rsplit('.', 1)[0]}_{i+1}.csv"
        df_subset.to_csv(new_filename, index=False)
        send_telegram_message(telegram_bot_token, telegram_chat_id, f"Создан файл {new_filename}")

telegram_bot_token = "6923028701:AAEj65_gjGrd-2L_BoA0YfXENFAqOAHHWU0"
telegram_chat_id = "-1001998959723"

# Запуск первого скрипта
try:
    result = subprocess.run(["python3", "SQL_python_download_v1.py"], check=True, capture_output=True)
    filename = result.stdout.strip()  # Считывание названия файла из вывода
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт выгрузки SQL  выполнен успешно, создан файл {filename} 💹")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте SQL. Данные НЕ обновлены. 🚫")

#Интервенция в аналитику. Принудительная обработка файла который берется не из базы данных. Удалить по окончанию
#filename = 'data-30-10-15-11.csv'


# Запуск второго скрипта с передачей файла в качестве аргумента
try:
    print('ОБРАБОТКА ФАЙЛА', filename)
    result = subprocess.run(["python3", "converting_signals.py", filename], check=True)
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт converting_signals.py выполнен успешно \n Данные отредактированы. 💹 \n Скачиваю рыночные данные по монетам...")
    final_filename = "FINALbetween_scripts_1_Modified_FINAL.csv" 
        # Вызов функции для разделения файла
   # split_csv_file(final_filename)
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте скачивания цены и редактирования 🚫")

# Остальные скрипты...
# Запуск третьего скрипта с передачей файла в качестве аргумента
try:
    result = subprocess.run(["python3", "updating_market_data_004.py"], check=True)
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт updating_market_data.py выполнен. \n Рыночные данные скачены 💹")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте скачивания рыночных данных 🚫")


try:
    result = subprocess.run(["python3", "SQL_python_download_results.py"], check=True, capture_output=True)
    filename = result.stdout.strip()  # Считывание названия файла из вывода
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт выгрузки SQL  c результатами выполнен успешно, файл создан 💹")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте SQL. Данные НЕ обновлены. 🚫")


try:
    result = subprocess.run(["python3", "merge_FIN_res.py"], check=True, capture_output=True)
    filename = result.stdout.strip()  # Считывание названия файла из вывода
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт мерджа выполнен успешно 💹")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте мерджа 🚫")


#Четртый скрипт аналитики на R
try:
    result = subprocess.run(["python3", "creating_analytics.py"], check=True)
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт аналитики на R выполнен 💹 \n Анализ доступен в файле.")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте аналитики на R 🚫")

#Пятый скрипт загрузки данных в таблицу
try:
    result = subprocess.run(["python3", "import2.py"], check=True)
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт загрузки результатов в БД выполнен 💹 \n")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка загрузки результатов в БД  🚫")
    
try:
    result = subprocess.run(["python3", "SQL_python_download_50_days.py"], check=True, capture_output=True)
    filename = result.stdout.strip()  # Считывание названия файла из вывода
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт выгрузки SQL  c результатами за 50 дней - выполнен 💹")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте SQL 50 дней. Данные НЕ выгружены. 🚫")

file_name = 'analytics_filter.csv'
#Пятый скрипт по созданию фильтров для торговли
try:
    result = subprocess.run(["python3", "filters_count.py", file_name], check=True)
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Скрипт подсчета каналов выполнен 💹 \n Файл будет перемещен в торговый скрипт")
except subprocess.CalledProcessError:
    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Ошибка в скрипте подсчета каналов 🚫")

#Финальная часть перемещения файла фильтров
operations_code = """
import os
import shutil

try:
    source_file = '/root/my_test/fully_automated_analytics/strategy1/filter.txt'
    renamed_file_in_same_dir = '/root/my_test/fully_automated_analytics/strategy1/authorized_channels.txt'
    os.rename(source_file, renamed_file_in_same_dir)
    print(f'Файл {source_file} был переименован в {renamed_file_in_same_dir}')


    target_directory = '/root/my_test/trading_process/authorized_channels.txt'
    shutil.move(renamed_file_in_same_dir, target_directory)
    print(f'Файл {renamed_file_in_same_dir} был перемещен в {target_directory}')

    # Удаляем папку strategy1
    folder_to_remove = './strategy1'
    shutil.rmtree(folder_to_remove)
    print(f'Папка {folder_to_remove} была успешно удалена')

    file_name = 'data_results_SL1TP3-3-4.csv'
    #os.remove(filename)
    #os.remove(file_name)

    #возвращаем дирректориюю strategy1 для будуущего анализа
    target_dir = os.path.join('/root/my_test/fully_automated_analytics','strategy1')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Директория {target_dir} была успешно создана.")

    shutil.copy('./setup.txt', './strategy1/setup.txt')
    print(f"Файл {source_file_path} был скопирован в {target_file_path}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
"""

#try:
 #   # Запуск кода как субпроцесс
  #  result = subprocess.run(['python3', '-c', operations_code], check=True, text=True, capture_output=True)
  #  print(result.stdout)
   # send_telegram_message(telegram_bot_token, telegram_chat_id, f"Файлы перемещены, дирректории перезапущены 💹 \n Ждем 24 часа до перезапуска")
#except subprocess.CalledProcessError as e:
#    send_telegram_message(telegram_bot_token, telegram_chat_id, f"Прерван процесс перестановки файлов или перезапуска дирректорий \n Ошибка при выполнении кода: {e.output} 🚫")
