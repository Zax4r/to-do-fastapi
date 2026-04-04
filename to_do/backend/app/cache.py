import redis.asyncio as redis
import json


redis_client: redis.Redis | None = None

async def init_redis(url):
    global redis_client
    redis_client = redis.from_url(url)

async def close_redis():
    if redis_client:
        await redis_client.close()


async def get_cached(key):
    data = await redis_client.get(key)
    return json.loads(data) if data else None

async def set_cached(key, value, TTL = 300):
    data = json.dumps(value, default=str)
    await redis_client.set(key, data, ex=TTL)
