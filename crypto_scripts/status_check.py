import psutil
import asyncio
from handlers.telegram_bot import check_binance_tg

# Путь к скриптам для проверки
scripts_to_check = [
    "/opt/my_test/modern_trading/monitornig_last.py",
    "/opt/my_test/binance-check.py",
    "/opt/my_test/postgres_upload.py",
    "/opt/my_test/check_redis.py",
    "main.py"
]

async def check_scripts():
    active_scripts = []

    # Проверка запущенных процессов
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline:  # Ensure cmdline is not None
                for script in scripts_to_check:
                    if script in cmdline:
                        active_scripts.append(script)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Формирование сообщения
    message = ""
    inactive_script_exists = False
    for script in scripts_to_check:
        status = "✅" if script in active_scripts else "❌"
        if status == "❌":
            inactive_script_exists = True
        message += f"{script}: {status}\n"

    # Отправка сообщения в Telegram, если есть неактивные скрипты
    if inactive_script_exists:
        await check_binance_tg("Статус скриптов:\n" + message)

async def periodic_main(interval):
    while True:
        await check_scripts()
        print('11111')
        await asyncio.sleep(interval)

if __name__ == '__main__':
    asyncio.run(periodic_main(60))
