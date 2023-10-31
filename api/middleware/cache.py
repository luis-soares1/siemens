from common.settings.config import app_settings
import redis.asyncio as redis
import pickle as p


class Cache:
    def __init__(self) -> None:
        self.redis_pool = None

    async def create_redis_pool(self):
        REDIS_URL = f"redis://{app_settings.cache_host}:{app_settings.redis_port}"
        connection_pool = redis.ConnectionPool.from_url(
            REDIS_URL)
        self.redis_pool = redis.Redis(
            connection_pool=connection_pool)

    async def close_redis_pool(self):
        if self.redis_pool:
            await self.redis_pool.close()
            await self.redis_pool.wait_closed()

    async def put(self, key, value, ttl):
        result = await self.redis_pool.set(key, p.dumps(value), ex=ttl)
        return bool(result)

    async def get(self, key):
        results = await self.redis_pool.get(key)
        if results:
            print('It was cached', p.loads(results))
            return p.loads(results)
        return None

    async def clear_all_cache(self):
        await self.redis_pool.flushall()

cache = Cache()
