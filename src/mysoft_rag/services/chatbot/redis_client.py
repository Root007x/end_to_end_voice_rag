import json
from fastapi import FastAPI


redis_client = None


async def init_redis(app: FastAPI):
    global redis_client
    redis_client = app.state.redis_client


async def set_cache(key, value, expire: int = 3600):
    await redis_client.set(key, json.dumps(value), ex=expire)


async def get_cache(key):
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None
