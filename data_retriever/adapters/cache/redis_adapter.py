import json
import redis
from ports.caching import CachePort


class RedisAdapter(CachePort):
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)

    def get(self, key: str):
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: dict, expiration: int = 3600):
        self.redis.setex(key, expiration, json.dumps(value))


def init_cache(redis_url):
    redis_client = redis.from_url(redis_url)
    redis_client.ping()
    return RedisAdapter(redis_url)
