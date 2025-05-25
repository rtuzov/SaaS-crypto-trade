import csv
import os, sys
from datetime import datetime
from trading_process.open_positions_hash_1_account import open_futures_trade as open_futures_position
from trading_process.trading_open_test_002_RT import open_futures_position1
from trading_process.trading_open_test_002_RT_v2 import open_futures_position2

def read_authorized_channels():
    with open(os.path.join(os.path.dirname(__file__), 'authorized_channels.txt'), 'r') as file:
        return [line.strip() for line in file]



def is_channel_authorized(chat_id):
    chat_id = abs(chat_id)
    print(chat_id)
    authorized_channels = read_authorized_channels()
    #return str(chat_id) in authorized_channels
    return true

def open_trade(coin, direction):
    print('Authorization SUCCESS!')
    pass

def save_unauthorized_trade(chat_id, message_id, coin, direction):
    with open('unauthorized_to_trade.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), chat_id, message_id, coin, direction])

def authorized_trades_with_id(chat_id, message_id, coin, direction):
    with open('authorized_trades_with_id.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), chat_id, message_id, coin, direction])

async def process_trade(chat_id, message_id, coin, direction):
    #if is_channel_authorized(chat_id):
    if True:
        print('AUTH COMPLETE')
        print(coin, direction)
        authorized_trades_with_id(chat_id, message_id, coin, direction)
        #open_futures_position(message_id, coin, direction)
        print("SIMPLE HELLO")
        #open_futures_position1(coin, direction)
        #open_futures_position2(coin, direction)

    else:
        print('FAIL AUTH TRADE')
        save_unauthorized_trade(chat_id, message_id, coin, direction)

# Пример использования
#process_trade('1001912770861','9877' ,'BTCUSDT', 'sell')
