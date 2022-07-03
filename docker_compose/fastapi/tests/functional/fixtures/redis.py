import aioredis
import pytest

from .settings import settings


@pytest.fixture
def flush_redis(redis_client: aioredis.Redis):
    async def inner():
        await redis_client.flushall()

    return inner


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20)

    yield redis

    redis.close()
    await redis.wait_closed()
