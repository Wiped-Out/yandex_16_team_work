import json
from abc import ABC, abstractmethod

from aioredis import Redis


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class BaseRedisStorage(AsyncCacheStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, **kwargs):
        return await self.redis.get(key=key)

    async def set(self, key: str, value: str, expire: int, **kwargs):
        return await self.redis.set(key=key, value=value, expire=expire)


class BaseCacheStorage:
    def __init__(self, cache: AsyncCacheStorage, **kwargs):
        super().__init__(**kwargs)

        self.cache = cache
        self.CACHE_EXPIRE_IN_SECONDS = 60 * 5

    async def get_one_item_from_cache(self, cache_key: str, model):
        data = await self.cache.get(key=cache_key)

        if not data:
            return None

        return model.parse_raw(data)

    async def put_one_item_to_cache(self, cache_key: str, item):
        await self.cache.set(
            key=cache_key,
            value=item.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )

    async def get_items_from_cache(self, cache_key: str, model):
        data = await self.cache.get(key=cache_key)
        if not data:
            return []

        return [model.parse_raw(item) for item in json.loads(data)]

    async def put_items_to_cache(self, cache_key: str, items: list):
        await self.cache.set(
            key=cache_key,
            value=json.dumps([item.json() for item in items]),
            expire=self.CACHE_EXPIRE_IN_SECONDS,
        )
