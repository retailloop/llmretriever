import json
import redis.asyncio as redis
from ports.caching import CachePort


class RedisAdapter(CachePort):
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str):
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: dict, expiration: int = 3600):
        await self.redis.setex(key, expiration, json.dumps(value))


async def init_cache(redis_url):
    redis_client = redis.from_url(redis_url)
    await redis_client.ping()
    return RedisAdapter(redis_url)
