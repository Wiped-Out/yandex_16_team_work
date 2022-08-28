import json
from abc import ABC, abstractmethod

from extensions.tracer import _trace
from redis import Redis
from redis.client import Pipeline


class CachePipeline(ABC):
    @abstractmethod
    def incr(self, key: str, amount: int, **kwargs):
        pass

    @abstractmethod
    def expire(self, key: str, expire: int, **kwargs):
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass


class CacheStorage(ABC):
    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def pipeline(self):
        pass


class BaseRedisPipeline(CachePipeline):
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def incr(self, key: str, amount: int, **kwargs):
        self.pipeline.incr(key, amount)

    def expire(self, key: str, expire: int, **kwargs):
        self.pipeline.expire(key, expire)

    def execute(self):
        return self.pipeline.execute()


class BaseRedisStorage(CacheStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, key: str, **kwargs):
        return self.redis.get(name=key)

    def set(self, key: str, value: str, expire: int, **kwargs):
        return self.redis.set(name=key, value=value, ex=expire)

    def close(self):
        self.redis.close()

    def pipeline(self) -> CachePipeline:
        return BaseRedisPipeline(pipeline=self.redis.pipeline())


class BaseCacheStorage:
    def __init__(self, cache: CacheStorage, **kwargs):
        super().__init__(**kwargs)

        self.cache = cache
        self.CACHE_EXPIRE_IN_SECONDS = 10

    @_trace()
    def get_one_item_from_cache(self, cache_key: str, model):
        data = self.cache.get(key=cache_key)

        if not data:
            return None

        return model.parse_raw(data)

    @_trace()
    def put_one_item_to_cache(self, cache_key: str, item, expire=None):
        self.cache.set(
            key=cache_key,
            value=item.json(),
            expire=self.CACHE_EXPIRE_IN_SECONDS if expire is None else expire,
        )

    @_trace()
    def get_items_from_cache(self, cache_key: str, model):
        data = self.cache.get(key=cache_key)
        if not data:
            return []

        return [model.parse_raw(item) for item in json.loads(data)]

    @_trace()
    def put_items_to_cache(self, cache_key: str, items: list, expire=None):
        self.cache.set(
            key=cache_key,
            value=json.dumps([item.json() for item in items]),
            expire=self.CACHE_EXPIRE_IN_SECONDS if expire is None else expire,
        )
