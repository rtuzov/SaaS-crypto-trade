from telegram import Bot
from config import TOKEN, TOKEN1

# CHANNEL_ID = '@something_and_something' # Это мой канал
CHANNEL_ID = -1001969410877 # Замените на ID вашего канала
MAIN_CHANNEL_ID = -1001797308199
LINK_CHANNEL_ID = -1001827812662
SPOT_CHANNEL_ID = -1002051169409
ERROR_CHANNEL_ID = -1002037984731
POSITION_TRADE_GROUP_ID = -4264984493
print('hi')
bot = Bot(token=TOKEN)
bot1 = Bot(token=TOKEN1)
print("hi2")

async def send_to_channel(message):
    await bot.send_message(chat_id=CHANNEL_ID, text=message)

#async def send_to_channel(text):
 #   await bot.send_message(chat_id=CHANNEL_ID, text=text)
  #  print("hi3")

async def send_to_main_channel(text):
    await bot.send_message(chat_id=MAIN_CHANNEL_ID, text=text)
    print("hi_to_main")

async def send_to_channel_links(text):
    await bot1.send_message(chat_id=LINK_CHANNEL_ID, text=text)
    print("hi_to_links")
    
async def send_to_channel_spot(text):
    await bot1.send_message(chat_id=SPOT_CHANNEL_ID, text=text)
    print("hi_to_spot")

async def send_to_error(error):
    await bot.send_message(chat_id=ERROR_CHANNEL_ID, text=error)
    print("hi_to_error")

async def open_trade_tg(error):
    await bot.send_message(chat_id=ERROR_CHANNEL_ID, text=error)
    print("open_trade")

async def check_binance_tg(message):
    await bot1.send_message(chat_id=POSITION_TRADE_GROUP_ID, text=message)
    print("check_binance")

print("hi5")
