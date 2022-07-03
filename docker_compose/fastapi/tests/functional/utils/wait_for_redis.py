import aioredis
from aioredis import Redis

from settings import settings
from .utils import backoff_on_true, backoff


class RedisManager:
    """Контекстный менеджер для работы с Redis"""

    @backoff()
    async def connect(self):
        self.connection = await aioredis.create_redis_pool((
            settings.REDIS_HOST, settings.REDIS_PORT
        ), minsize=10, maxsize=20)

    async def __aenter__(self) -> Redis:
        await self.connect()
        return self.connection

    async def __aexit__(self, error: Exception, value: object, traceback: object):
        self.connection.close()
        await self.connection.wait_closed()


@backoff_on_true()
async def wait_for_redis():
    async with RedisManager() as redis:
        return await redis.ping()
