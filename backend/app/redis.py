from app.settings import get_settings
from redis.asyncio import Redis

settings = get_settings()

async def init_redis():
    global redis
    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
    )

async def close_redis():
    global redis
    if redis:
        await redis.close()

async def get_cache(key: str):
    if redis:
        return await redis.get(key)

async def set_cache(key: str, value: str, ttl: int = None):
    await redis.set(key, value, ex=ttl)

async def delete_cache(key: str):
    if redis:
        await redis.delete(key)