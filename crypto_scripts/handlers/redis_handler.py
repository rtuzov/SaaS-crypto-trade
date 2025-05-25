import aioredis
from config import REDIS_URL
import logging

logger = logging.getLogger('my_bot')

async def create_redis_connection(db):
    return aioredis.from_url(f"{REDIS_URL}/{db}", encoding="utf-8", decode_responses=True)

async def get_value(redis, key):
    return await redis.get(key)

async def save_to_redis(redis, key, value):
    await redis.set(key, value)
    await redis.expire(key, 24*60*60)  # Set key expiration to 24 hours

async def get_all_keys(redis):
    keys = await redis.keys('*')
    return keys

async def delete_key(redis, key):
    await redis.delete(key)

async def save_to_redis_coin(redis, key, value):
    await redis.set(key, value)
    
async def save_to_redis_trade(redis, key):
    await redis.set(key,"")
    
    
async def save_to_redis_open_trade(redis, key, value):
    await redis.set(key, value)