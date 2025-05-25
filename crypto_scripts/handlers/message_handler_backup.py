import time
import logging
import json
import sys
import datetime
from pyrogram import Client
from pyrogram.types import Message, Chat, User
from pyrogram.enums import ChatType
from database import SessionLocal, MessageScraping, MessageScrapingGPT, MessageScrapingGPTValue, ErrorMessages
from utils.openai_utils import chat_gpt
from handlers.redis_handler import create_redis_connection, save_to_redis, get_value, get_all_keys, delete_key
from handlers.telegram_bot import send_to_channel_links, send_to_channel_spot, send_to_main_channel, send_to_channel
import signal_filter
import asyncio
from sqlalchemy.future import select
from config import DEBUG

logger = logging.getLogger('my_bot')

def message_to_dict(message: Message) -> dict:
    message_dict = {
        "message_id": message.id,
        "date": message.date.isoformat() if message.date else None,
        "chat": {
            "id": message.chat.id,
            "title": message.chat.title,
            "type": message.chat.type.value  # Преобразование типа чата в строку
        },
        "from_user": {
            "id": message.from_user.id,
            "is_bot": message.from_user.is_bot,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "username": message.from_user.username,
            "language_code": message.from_user.language_code
        } if message.from_user else None,
        "text": message.text,
        "caption": message.caption
    }
    return message_dict

def dict_to_message(message_dict: dict) -> Message:
    from pyrogram.types import Chat, User, Message

    message_dict['date'] = datetime.fromisoformat(message_dict['date'])
    chat_dict = message_dict.pop('chat')
    from_user_dict = message_dict.pop('from_user', None)

    chat_type = ChatType(chat_dict['type'])

    chat = Chat(id=chat_dict['id'], type=chat_type, title=chat_dict['title'])

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


async def handle_text_messages(client: Client, message: Message):
    logger.info("Handling message in handle_text_messages")
    async with SessionLocal() as session:
        try:
            text = extract_message_text(message)
            if not text:
                logger.warning("No text found in message")
                return
            logger.info("Processing message: %s", text)

            redis_queue = await create_redis_connection(db=0)
            redis_sql = await create_redis_connection(db=1)

            if await check_and_handle_forwarded_message(redis_queue, message):
                return
            text_lower = text.lower().replace('\n', ' ')
            await check_links_and_spot(message, text)

            cat = check_keywords(text_lower)
            # Сериализация message в JSON
            message_json = json.dumps(message_to_dict(message))


            redis_key = f"{message.chat.id}:{message.id}"
            redis_value = f"{message.date}|{message.chat.id}|{message.chat.title}|{message.id}|{text}|{cat}|{message_json}"
            await save_to_redis(redis_queue, redis_key, redis_value)

            if cat:
                await process_message(redis_sql, message, text, text_lower, cat)
        except Exception as e:
            logger.error("Error processing message: %s", e)
            async with SessionLocal() as session:
                await save_error_message(session, message, redis_sql)


def extract_message_text(message: Message):
    logger.info("Extracting message text")
    try:
        text_replace = None
        if message.text:
            if DEBUG:
                print(f'{sys._getframe().f_lineno}|поймал текст|')
            text = message.text
            text_lower = text.lower()
            text_replace = text_lower.replace('\n', ' ')
        elif message.photo:
            if DEBUG:
                print(f'{sys._getframe().f_lineno}|поймал фото|')
            if message.caption:
                text = message.caption
                text_lower = text.lower()
                text_replace = text_lower.replace('\n', ' ')
        elif message.video:
            if DEBUG:
                print(f'{sys._getframe().f_lineno}|поймал видео|')
            if message.caption:
                text = message.caption
                text_lower = text.lower()
                text_replace = text_lower.replace('\n', ' ')
        elif message.animation:
            if DEBUG:
                print(f'{sys._getframe().f_lineno}|поймал анимацию|')
            if message.caption:
                text = message.caption
                text_lower = text.lower()
                text_replace = text_lower.replace('\n', ' ')

        elif message.document:
            if DEBUG:
                print(f'{sys._getframe().f_lineno}|поймал анимацию|')
            if message.caption:
                text = message.caption
                text_lower = text.lower()
                text_replace = text_lower.replace('\n', ' ')
        if text_replace:
            return text_replace
        else:
            logger.warning("No text or caption found in message")
            return None
    except Exception as e:
        logger.error(f"Error extracting message text: {e}")
        return None


async def check_and_handle_forwarded_message(redis, message: Message):

    logger.info("Checking if message is forwarded")
    if message.forward_from or message.forward_from_chat:
        key_str = f"{message.chat.id}:{message.reply_to_message_id}".encode('utf-8')
        value = await redis.get(key_str)
        if value:
            logger.debug("Forwarded message found in Redis: %s", value)
            return True
    return False


async def check_links_and_spot(message: Message, text: str):
    logger.info("Checking links and spot keywords in message")
    if message.chat.id != -1001827812662:
        await check_links(text)
    if message.chat.id != -1002051169409:
        await check_spot(text)

async def check_links(text: str):
    logger.info("Checking links in message")
    keywords_links = ['t.me/', 'http', 'ссылк', 'link']
    for key in keywords_links:
        if key in text:
            await send_to_channel_links(text)
            return key
    return ''

async def check_spot(text: str):
    logger.info("Checking spot keywords in message")
    keywords_spot = ['spot', 'спот']
    for key in keywords_spot:
        if key in text:
            await send_to_channel_spot(text)
            return key
    return ''

def check_keywords(text: str):
    logger.info("Checking keywords in message")
    keywords = ['long', 'short', 'шорт', 'лонг', '📈', '📉', 'lоng', 'shоrt', '(long)', '(short)', 'signal', 'сигнал', 'депо', 'депозит', 'сетап', 'setup', 'risk', 'риск',  'buy',  'sell', 'покуп', 'продаж', 'купить', 'продать', 'купи', 'прода']
    for key in keywords:
        if key in text:
            return key
    return ''

async def process_message(redis_sql, message, text, text_lower, cat):
    logger.info("Processing message with category: %s", cat)
   # money = check_money(text_lower).lower()
    async with SessionLocal() as session:
       # if not await is_duplicate_message1(session, message):
        new_message = MessageScraping(
            channel_id=message.chat.id,
            channel_name=message.chat.title,
            message_id=message.id,
            message_text=text,
        )
        session.add(new_message)
        await session.commit()

        # Save to redis SQL database
        redis_key = f"MessageScraping:{message.chat.id}:{message.id}"
        redis_value = f"{datetime.datetime.now()}|{message.chat.id}|{message.chat.title}|{message.id}|{text}"
        print(redis_value)
        await save_to_redis(redis_sql, redis_key, redis_value)

        logger.info("Keyword found: %s", cat)
        logger.info("Sending message to chat_gpt: %s", text)
        start_time = time.time()

        gpt_response = await chat_gpt(text)
        await process_gpt_response(session, redis_sql, message, text, gpt_response, start_time, cat)

def check_money(text: str):
    logger.info("Checking money keywords in message")
    list_money = ['1000BTTC']
    for key in list_money:
        if key.lower() in text:
            return key
    return ''

async def save_error_message(session, message, redis_sql):
    logger.info("Saving error message")
    text = extract_message_text(message)
    #if not await is_duplicate_message2(session, message):
    error_message = ErrorMessages(
        channel_id=message.chat.id,
        channel_name=message.chat.title,
        message_id=message.id,
        message_text=text
    )
    session.add(error_message)
    await session.commit()

    redis_key = f"MessageScrapingGPT:{message.chat.id}:{message.id}"
    redis_value = f"{datetime.datetime.now()}|{message.chat.id}|{message.chat.title}|{message.id}"
    await save_to_redis(redis_sql, redis_key, redis_value)

async def process_gpt_response(session, redis_sql, message, text, gpt_response, start_time, cat):
    logger.info("Processing GPT response")
    elapsed_time = time.time() - start_time
    gpt_response_time = datetime.datetime.now() + datetime.timedelta(seconds=elapsed_time)
   # if not await is_duplicate_message3(session, message):
    new_message = MessageScrapingGPT(
        channel_id=message.chat.id,
        channel_name=message.chat.title,
        message_id=message.id,
        message_text=text,
        gpt_response=gpt_response,
        gpt_response_time=gpt_response_time
    )
    session.add(new_message)
    await session.commit()

    # Save to redis SQL database
    redis_key = f"MessageScrapingGPT:{message.chat.id}:{message.id}"
    redis_value = f"{datetime.datetime.now()}|{message.chat.id}|{message.chat.title}|{message.id}|{text}|{gpt_response}|{gpt_response_time}"
    await save_to_redis(redis_sql, redis_key, redis_value)

    values_dict = parse_gpt_response(gpt_response)

    await save_gpt_values(session, redis_sql, message, text, gpt_response, values_dict, gpt_response_time, cat)
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


async def save_gpt_values(session, redis_sql, message, text, gpt_response, values_dict, gpt_response_time, cat):

    logger.info("Saving GPT values")

    # Загрузка JSON-словарей
    try:
        with open('dictionary.json', 'r') as f:
            loaded_dictionary = json.load(f)
            loaded_dictionary = {k.lower(): v for k, v in
                                 loaded_dictionary.items()}  # Приведение ключей к нижнему регистру
            logger.info("Loaded dictionary.json")
    except Exception as e:
        logger.error(f"Error loading dictionary.json: {e}")
        return

    try:
        with open('new_dictionary_direction_gpt.json', 'r') as fi:
            loaded_direction_gpt = json.load(fi)
            loaded_direction_gpt = {k.lower(): v for k, v in
                                    loaded_direction_gpt.items()}  # Приведение ключей к нижнему регистру
            logger.info("Loaded new_dictionary_direction_gpt.json")
    except Exception as e:
        logger.error(f"Error loading new_dictionary_direction_gpt.json: {e}")
        return

    logger.info(f"GPT Values Dictionary: {values_dict}")

    try:
        crypto_currency_gpt = values_dict.get("Криптовалюта", "").lower()
        if not crypto_currency_gpt:
            raise KeyError("Ключ 'Криптовалюта' не найден в values_dict")
        logger.info(f"Original Crypto Currency: {crypto_currency_gpt}")

#       logger.info(f"Loaded dictionary keys: {list(loaded_dictionary.keys())}")
        if crypto_currency_gpt in loaded_dictionary:
            crypto_currency_gpt = loaded_dictionary[crypto_currency_gpt]
            logger.info(f"Translated Crypto Currency: {crypto_currency_gpt}")
        else:
            logger.warning(f"Crypto Currency '{crypto_currency_gpt}' not found in dictionary")

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

        direction_gpt = values_dict.get("Направление сделки", "").lower()
        if not direction_gpt:
            raise KeyError("Ключ 'Направление сделки' не найден в values_dict")
        if direction_gpt.endswith("."):
            direction_gpt = direction_gpt[:-1]

        if direction_gpt in loaded_direction_gpt:
            direction_gpt = loaded_direction_gpt[direction_gpt]

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

       # if not await is_duplicate_message4(session, message):
        new_message = MessageScrapingGPTValue(
            channel_id=message.chat.id,
            channel_name=message.chat.title,
            message_id=message.id,
            message_text=text,
            gpt_response=gpt_response,
            crypto_currency_gpt=crypto_currency_gpt,
            direction_gpt=direction_gpt,
            enter_gpt=enter_gpt,
            take_profit_gpt=take_profit_gpt,
            stop_loss_gpt=stop_loss_gpt,
            leverage_gpt=leverage_gpt,
            coin_cost='unknown',
            averaging=averaging,
            signal=signal
        )
        session.add(new_message)
        await session.commit()


        # Save to redis SQL database
        redis_key = f"MessageScrapingGPTValue:{message.chat.id}:{message.id}"
        redis_value = f"{datetime.datetime.now()}|{message.chat.id}|{message.chat.title}|{message.id}|{text}|{gpt_response}|{crypto_currency_gpt}|{direction_gpt}|{enter_gpt}|{take_profit_gpt}|{stop_loss_gpt}|{leverage_gpt}|{'unknown'}|{averaging}|{signal}"
        await save_to_redis(redis_sql, redis_key, redis_value)


        # Вызов функции send_to_telegram с необходимыми значениями
        await send_to_telegram(message, crypto_currency_gpt, direction_gpt, enter_gpt, take_profit_gpt, stop_loss_gpt,
                               leverage_gpt, averaging, signal)



    except KeyError as e:
        logger.error(f"Key error: {e} not found in values_dict")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


async def send_to_telegram(message, crypto_currency_gpt, direction_gpt, enter_gpt, take_profit_gpt, stop_loss_gpt, leverage_gpt, averaging, signal):
    logger.info("Sending message to Telegram channels")

    telegram_text_modified = f"""
ИСХОДНИК: {message.text}
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

    if signal_filter.check_signal(crypto_currency_gpt, direction_gpt):
        await send_to_channel(telegram_text_modified)
        await send_to_main_channel(telegram_text_production)
       # await process_t(message.chat.id, message.id, crypto_currency_gpt, direction_gpt)

    # Удаление ключа из Redis перед отправкой сообщения
    redis_queue = await create_redis_connection(db=0)
    redis_key = f"{message.chat.id}:{message.id}"
    await delete_key(redis_queue, redis_key)


# Добавление функции для периодической проверки записей в Redis
async def check_redis_records():
    while True:
        try:
            redis = await create_redis_connection()
            keys = await get_all_keys(redis)
            if keys:
                for key in keys:
                    redis_value = await get_value(redis, key)
                    values = redis_value.split("|")
                    message_date, message_chat_id, message_chat_title, message_id, text, cat, message_json = values
                    message_dict = json.loads(message_json)
                    message = dict_to_message(message_dict)
                    await process_message(redis, message, text, text.lower().replace('\n', ' '), cat)
        except Exception as e:
            logger.error("Error while checking Redis records: %s", e)
        await asyncio.sleep(45)  # Добавьте задержку, чтобы не перегружать Redis


async def is_duplicate_message1(session, message):
    stmt = select(MessageScraping).filter_by(channel_id=message.chat.id, message_id=message.id)
    result = await session.execute(stmt)

    existing_message = result.scalars().first()
    if existing_message:
        logger.info("Duplicate message found, skipping")
        return True
    return False

async def is_duplicate_message2(session, message):
    stmt = select(ErrorMessages).filter_by(channel_id=message.chat.id, message_id=message.id)
    result = await session.execute(stmt)
    existing_message = result.scalars().first()
    if existing_message:
        logger.info("Duplicate message found, skipping")
        return True
    return False

async def is_duplicate_message3(session, message):
    stmt = select(MessageScrapingGPT).filter_by(channel_id=message.chat.id, message_id=message.id)
    result = await session.execute(stmt)
    existing_message = result.scalars().first()
    if existing_message:
        logger.info("Duplicate message found, skipping")
        return True
    return False

async def is_duplicate_message4(session, message):
    stmt = select(MessageScrapingGPTValue).filter_by(channel_id=message.chat.id, message_id=message.id)
    result = await session.execute(stmt)
    existing_message = result.scalars().first()
    if existing_message:
        logger.info("Duplicate message found, skipping")
        return True
    return False