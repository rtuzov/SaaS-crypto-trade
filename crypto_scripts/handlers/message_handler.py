import time
import logging
import json
import sys
import csv
import datetime
from telethon import TelegramClient, events, functions
from dateutil.parser import isoparse
from database import SessionLocal, MessageScraping, MessageScrapingGPT, MessageScrapingGPTValue, ErrorMessages
from utils.openai_utils import chat_gpt
from handlers.redis_handler import create_redis_connection, save_to_redis, get_value, get_all_keys, delete_key
from handlers.telegram_bot import send_to_channel_links, send_to_channel_spot, send_to_main_channel, send_to_channel, send_to_error
import signal_filter
from trading_process.validating_trade import process_trade as process_t
import asyncio
from sqlalchemy.future import select
from config import DEBUG

logger = logging.getLogger('my_bot')

'''
def message_to_dict(message: Message, text) -> dict:
    def replace_pipe_with_ampersands(text: str) -> str:
        return text.replace('|', '&&') if text else 'none'

    message_dict = {
        "message_id": message_id,
        "date": message.date.isoformat() if message.date else None,
        "chat": {
            "id": chat_id,
            "chat_title": replace_pipe_with_ampersands(chat_title),
            "type": message.chat.type.value  # Convert chat type to string
        },
        "from_user": {
            "id": message.from_user.id,
            "is_bot": message.from_user.is_bot,
            "first_name": message.from_user.first_name,
            "last_name": replace_pipe_with_ampersands(message.from_user.last_name),
            "username": message.from_user.username,
            "language_code": message.from_user.language_code
        } if message.from_user else None,
        "text": replace_pipe_with_ampersands(text) if message.text else None,
        "caption": replace_pipe_with_ampersands(text) if message.caption else None
    }

    return message_dict




def dict_to_message(message_dict: dict) -> Message:
    from pyrogram.types import Chat, User, Message

    message_dict['date'] = isoparse(message_dict['date'])
    chat_dict = message_dict.pop('chat')
    from_user_dict = message_dict.pop('from_user', None)

    chat_type = ChatType(chat_dict['type'])

    chat = Chat(id=chat_dict['id'], type=chat_type, chat_title=chat_dict['chat_title'])

    from_user = None
    if from_user_dict:
        from_user = User(**from_user_dict)

    return Message(
        id=message_dict['message_id'],
        date=message_dict['date'],
        chat=chat,
        from_user=from_user,
        text=message_dict['text'],
        caption=message_dict['caption']
    )
'''

async def handle_text_messages(event, text, chat_id, text_replace, text_original, chat_title, message_id, formatted_date):
    logger.info("Handling message in handle_text_messages")
    redis_queue = await create_redis_connection(db=1)
    redis_sql = await create_redis_connection(db=2)

    async with SessionLocal() as session:
        try:

            await check_links_and_spot(chat_id, text_original, text_replace)
            logger.info("Processing message: %s", text_replace)

            #if await check_and_handle_forwarded_message(redis_queue, event):
            #    return

            cat = check_keywords(text_replace)

            if cat and chat_id not in {-1001827812662, -1002051169409}:
                if chat_title is None:
                    chat_title = "None"
                # message_json = json.dumps(message_to_dict(event, text_original))
                redis_key = f"{chat_id}:{message_id}"
                redis_value = f"{formatted_date}|{chat_id}|{chat_title}|{message_id}|{text_original}|{cat}"

                checker = 'None'
                await save_to_redis(redis_queue, redis_key, redis_value)
                await process_message(redis_sql, text_replace, cat, chat_title, chat_id, message_id, text_original, checker)

        except Exception as e:
            logger.error("Error processing message: %s: %s - %s", e, chat_title, text_replace)
            if redis_sql:
                async with session:
                    await save_error_message(session, redis_sql, chat_title, text_original, chat_id, message_id)
'''
async def check_and_handle_forwarded_message(redis, message: Message):
    logger.info("Checking if message is forwarded")
    if message.forward_from or message.forward_from_chat:
        key_str = f"{chat_id}:{message.reply_to_message_id}".encode('utf-8')
        value = await redis.get(key_str)
        if value:
            logger.debug("Forwarded message found in Redis: %s", value)
            return True
    return False
'''

async def check_links_and_spot(chat_id, text_original, text_replace):
    logger.info("Checking links and spot keywords in message")
    if chat_id != -1001827812662:
        await check_links(text_original, text_replace)
    if chat_id != -1002051169409:
        await check_spot(text_original, text_replace)


async def check_links(text_original, text_replace):
    logger.info("Checking links in message")
    keywords_links = ['t.me/', 'http', 'ссылк', 'link']
    for key in keywords_links:
        if key in text_replace:
            await send_to_channel_links(text_original)
            return key
    return ''


async def check_spot(text_original, text_replace):
    logger.info("Checking spot keywords in message")
    keywords_spot = ['spot', 'спот']
    for key in keywords_spot:
        if key in text_replace:
            await send_to_channel_spot(text_original)
            return key
    return ''


def check_keywords(text_replace):
    logger.info("Checking keywords in message")
    
    keywords = ['long', 'short', 'шорт', 'лонг', '📈', '📉', 'lоng', 'shоrt', '(long)', '(short)', 'signal', 'сигнал',
                'депо', 'депозит', 'сетап', 'setup', 'risk', 'риск', 'buy', 'sell', 'покуп', 'продаж', 'купить',
                'продать', 'купи', 'прода', 'خدها' , 'يشتري', 'يبيع', 'طويل', 'قصير']
    keywords2 = ['take-profit target 6 ✅', 'take-profit target 5 ✅', 'take-profit target 4 ✅', 'take-profit target 3 ✅', 'take-profit target 7 ✅', 'take-profit target 8 ✅','target-5 reached', 'All take-profit targets achieved', 'achieved', 'достигнут', 'достигл','Target-5']

    
    # Check if any of the keywords are in text_replace
    for key in keywords:
        if key in text_replace:
            # If any of the keywords2 are also in text_replace, return an empty string
            for key2 in keywords2:
                if key2 in text_replace:
                    return ''
            # If none of the keywords2 are found, return the matched keyword from keywords
            return key
    
    return ''


async def process_message(redis_sql, text_replace, cat, chat_title, chat_id, message_id, text_original, checker):

    logger.info("Processing message with category: %s", cat)
    # money = check_money(text_lower).lower()
    async with SessionLocal() as session:
        # Save to redis SQL database
        redis_key = f"MessageScraping:{chat_id}:{message_id}"
        redis_value = f"{datetime.datetime.now()}|{chat_id}|{chat_title}|{message_id}|{text_replace}"
        await save_to_redis(redis_sql, redis_key, redis_value)

        logger.info("Keyword found: %s", cat)
        logger.info("Sending message to chat_gpt: %s", text_replace)
        start_time = time.time()

        gpt_response = await chat_gpt(text_original)
        await process_gpt_response(session, redis_sql, text_original, gpt_response, start_time, cat, chat_title, chat_id, message_id, checker)


def check_money(text: str):
    logger.info("Checking money keywords in message")
    list_money = ['1000BTTC']
    for key in list_money:
        if key.lower() in text:
            return key
    return ''


async def save_error_message(session, redis_sql, chat_title, text_original, chat_id, message_id):
    logger.info("Saving error message")
    text = text_original

    redis_key = f"ErrorMessages:{chat_id}:{message_id}"
    redis_value = f"{datetime.datetime.now()}|{chat_id}|{chat_title}|{message_id}"
    await save_to_redis(redis_sql, redis_key, redis_value)
    error = f"Ошибка при обработке {chat_id}: {message_id} - {chat_title}, {text}"
    await send_to_error(error)


async def process_gpt_response(session, redis_sql, text_original, gpt_response, start_time, cat, chat_title, chat_id, message_id, checker):
    logger.info("Processing GPT response")
    elapsed_time = time.time() - start_time
    gpt_response_time = datetime.datetime.now() + datetime.timedelta(seconds=elapsed_time)

    # Save to redis SQL database
    redis_key = f"MessageScrapingGPT:{chat_id}:{message_id}"
    redis_value = f"{datetime.datetime.now()}|{chat_id}|{chat_title}|{message_id}|{text_original}|{gpt_response}|{gpt_response_time}"
    await save_to_redis(redis_sql, redis_key, redis_value)

    values_dict = parse_gpt_response(gpt_response)

    await save_gpt_values(session, redis_sql, gpt_response, values_dict, chat_title, chat_id, message_id, text_original, checker)


# await send_to_telegram(message, values_dict)


def parse_gpt_response(gpt_response):
    logger.info("Parsing GPT response")
    values_list = gpt_response.split("\n")
    values_dict = {}
    for value in values_list:
        try:
            key, val = value.split(": ")
            values_dict[key] = val
        except ValueError:
            continue
    return values_dict


async def save_gpt_values(session, redis_sql, gpt_response, values_dict, chat_title, chat_id, message_id, text, checker):
    logger.info("Saving GPT values")

    # Загрузка JSON-словарей
    try:
        with open('/opt/my_test/dictionary.json', 'r') as f:
            loaded_dictionary = json.load(f)
            loaded_dictionary = {k.lower(): v for k, v in
                                 loaded_dictionary.items()}  # Приведение ключей к нижнему регистру
            logger.info("Loaded dictionary.json")
    except Exception as e:
        logger.error(f"Error loading dictionary.json: {e}")
        return

    try:
        with open('/opt/my_test/new_dictionary_direction_gpt.json', 'r') as fi:
            loaded_direction_gpt = json.load(fi)
            loaded_direction_gpt = {k.lower(): v for k, v in
                                    loaded_direction_gpt.items()}  # Приведение ключей к нижнему регистру
            logger.info("Loaded new_dictionary_direction_gpt.json")
    except Exception as e:
        logger.error(f"Error loading new_dictionary_direction_gpt.json: {e}")
        return

    logger.info(f"GPT Values Dictionary: {values_dict}")

    try:
        crypto_currency_gpt = values_dict.get("Криптовалюта", "").lower().replace(' ', '')
        if not crypto_currency_gpt:
            raise KeyError("Ключ 'Криптовалюта' не найден в values_dict")
        logger.info(f"Original Crypto Currency: {crypto_currency_gpt}")

        #       logger.info(f"Loaded dictionary keys: {list(loaded_dictionary.keys())}")
        if crypto_currency_gpt in loaded_dictionary:
            crypto_currency_gpt = loaded_dictionary[crypto_currency_gpt]
            logger.info(f"Translated Crypto Currency: {crypto_currency_gpt}")
        else:
            logger.warning(f"Crypto Currency '{crypto_currency_gpt}' not found in dictionary")
            # Append the not found currency to a CSV file
            with open('crypto_currency.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([crypto_currency_gpt])

        crypto_currency_gpt = crypto_currency_gpt.replace("/usdt", "").replace("_", "").replace("usdt", "").upper()
        if crypto_currency_gpt in ["BTC", "БИТОК", "БИТКОИН", "BITCOIN"]:
            for key in values_dict:
                values_dict[key] = values_dict[key].replace(",", "").replace(" ", "").replace("$", "")

        if crypto_currency_gpt in ["BTC", "БИТОК", "БИТКОИН", "BITCOIN"]:
            crypto_currency_gpt = crypto_currency_gpt.replace(",", "/").replace(" ", "/")

        if crypto_currency_gpt not in ["BTC", "БИТОК", "БИТКОИН", "BITCOIN"]:
            crypto_currency_gpt = crypto_currency_gpt.replace("$", "").replace("(", "").replace(",", "")
            if crypto_currency_gpt.endswith("."):
                crypto_currency_gpt = crypto_currency_gpt[:-1]
            if crypto_currency_gpt.endswith(" "):
                crypto_currency_gpt = crypto_currency_gpt[:-1]

        crypto_currency_gpt = crypto_currency_gpt.upper()

        direction_gpt = values_dict.get("Направление сделки", "").lower().replace(' ', '')
        if not direction_gpt:
            raise KeyError("Ключ 'Направление сделки' не найден в values_dict")
        if direction_gpt.endswith("."):
            direction_gpt = direction_gpt[:-1]

        if direction_gpt in loaded_direction_gpt:
            direction_gpt = loaded_direction_gpt[direction_gpt]
            logger.info(f"Translated Direction: {direction_gpt}")
        else:
            logger.warning(f"Direction  '{direction_gpt}' not found in dictionary")
            # Append the not found currency to a CSV file
            with open('direction_gpt.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([direction_gpt])


        enter_gpt = values_dict.get("Точка входа", "").lower()
        if not enter_gpt:
            raise KeyError("Ключ 'Точка входа' не найден в values_dict")
        if enter_gpt.endswith("."):
            enter_gpt = enter_gpt[:-1]

        if crypto_currency_gpt.lower() == "btc":
            enter_gpt = enter_gpt.replace(".", "").replace(" ", "")

        if "по рынку" in enter_gpt.lower() or "по маркету" in enter_gpt.lower():
            enter_gpt = "по рынку"

        if enter_gpt == 'по рынку' or enter_gpt.lower() == 'по рыночной цене' or enter_gpt.lower() == 'рынок' or enter_gpt.lower() == 'на усмотрение':
            enter_gpt = 'по рынку'

        enter_gpt = enter_gpt.replace("$", "").replace("/market", "").replace("entry", "").replace("USDT", "")

        take_profit_gpt = values_dict.get("Тейк-профит", "").lower()
        if not take_profit_gpt:
            raise KeyError("Ключ 'Тейк-профит' не найден в values_dict")
        take_profit_gpt = take_profit_gpt.replace("$", "")
        if take_profit_gpt.endswith("."):
            take_profit_gpt = take_profit_gpt[:-1]

        if crypto_currency_gpt.lower() == "btc":
            take_profit_gpt = take_profit_gpt.replace(".", "").replace(" ", "")

        stop_loss_gpt = values_dict.get("Стоп-лосс", "").lower()
        if not stop_loss_gpt:
            raise KeyError("Ключ 'Стоп-лосс' не найден в values_dict")
        stop_loss_gpt = stop_loss_gpt.replace("$", "")
        if stop_loss_gpt.endswith("."):
            stop_loss_gpt = stop_loss_gpt[:-1]

        if crypto_currency_gpt.lower() == "btc":
            stop_loss_gpt = stop_loss_gpt.replace(".", "").replace(" ", "")

        leverage_gpt = values_dict.get("Плечо", "").lower()
        if not leverage_gpt:
            raise KeyError("Ключ 'Плечо' не найден в values_dict")

        limit_orders = values_dict.get('Лимитные заявки', "").lower()
        if DEBUG:
            print(f'{sys._getframe().f_lineno}|Лимитные заявки|{limit_orders}|{type(limit_orders)}')

        averaging = values_dict.get('Усреднения', "").lower()
        if DEBUG:
            print(f'{sys._getframe().f_lineno}|Усреднения|{averaging}|{type(averaging)}')

        try:
            signal = values_dict.get('Сигнал', "").lower()



        except KeyError:
            signal = 'сигнал отсутствует'

        # Save to redis SQL database
        redis_key = f"MessageScrapingGPTValue:{chat_id}:{message_id}"
        redis_value = f"{datetime.datetime.now()}|{chat_id}|{chat_title}|{message_id}|{text}|{gpt_response}|{crypto_currency_gpt}|{direction_gpt}|{enter_gpt}|{take_profit_gpt}|{stop_loss_gpt}|{leverage_gpt}|{'unknown'}|{averaging}|{signal}"
        await save_to_redis(redis_sql, redis_key, redis_value)

        # Вызов функции send_to_telegram с необходимыми значениями
        await send_to_telegram(text, crypto_currency_gpt, direction_gpt, enter_gpt, take_profit_gpt, stop_loss_gpt,
                               leverage_gpt, averaging, signal, chat_id, message_id, chat_title, checker)



    except KeyError as e:
        logger.error(f"Key error: {e} not found in values_dict")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


async def send_to_telegram(text, crypto_currency_gpt, direction_gpt, enter_gpt, take_profit_gpt, stop_loss_gpt,
                           leverage_gpt, averaging, signal, chat_id, message_id, chat_title, checker):
    logger.info("Sending message to Telegram channels")

    telegram_text_modified = f"""
ЧАТ: {chat_title}:{chat_id}:{message_id}:checker={checker}
ИСХОДНИК: {text}
🎊 Выгодный сигнал:

Монета: 🪙 {crypto_currency_gpt} / USDT

Направление: {direction_gpt}

Вход:💰 {enter_gpt}
Тейк-профит:🎯 {take_profit_gpt}
Стоп-лосс: ❌ {stop_loss_gpt}
Плечо: 💪 {leverage_gpt}
Прибыльность: 💲 от 20%
Риск: 🟢 Низкий
    """
    telegram_text_production = f"""
Монета: {crypto_currency_gpt} / USDT

Направление: {direction_gpt}

Вход:💰 {enter_gpt}
Тейк-профит:🎯 {take_profit_gpt}
Стоп-лосс: ❌ {stop_loss_gpt}
Плечо: 💪 {leverage_gpt}
Прибыльность: 💲 от 20%
Риск: Низкий
    """
    message_sent_successfully = False

    try:
        if signal_filter.check_signal(crypto_currency_gpt, direction_gpt):
            await send_to_channel(telegram_text_modified)
            await send_to_main_channel(telegram_text_production)

         #   await process_t(chat_id, message_id, crypto_currency_gpt, direction_gpt)


            message_sent_successfully = True

        else:
            try:
                redis_queue = await create_redis_connection(db=1)
                redis_key = f"{chat_id}:{message_id}"
                await delete_key(redis_queue, redis_key)
                logger.info(f"Deleted key {redis_key} from Redis")
            except Exception as e:
                logger.error(f"Error deleting key {redis_key} from Redis: {e}")
    except Exception as e:
        logger.error(f"Error sending message to Telegram channels: {e}")
        message_sent_successfully = False

    if message_sent_successfully:
        try:
            redis_queue = await create_redis_connection(db=1)
            redis_key = f"{chat_id}:{message_id}"
            await delete_key(redis_queue, redis_key)
            logger.info(f"Deleted key {redis_key} from Redis")
        except Exception as e:
            logger.error(f"Error deleting key {redis_key} from Redis: {e}")
            error = f"Error deleting key {redis_key} from Redis: {e}"
            await send_to_error(error)
