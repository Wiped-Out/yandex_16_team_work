import aioredis

from settings import settings


async def wait_for_redis():
    redis = await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20)
    while not await redis.ping():
        pass
    redis.close()
    await redis.wait_closed()