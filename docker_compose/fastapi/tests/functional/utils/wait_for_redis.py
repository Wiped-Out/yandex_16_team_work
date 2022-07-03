import aioredis

from settings import settings
from utils.utils import backoff


@backoff
async def wait_for_redis():
    redis = await aioredis.create_redis_pool((
        settings.REDIS_HOST, settings.REDIS_PORT
    ), minsize=10, maxsize=20)
    redis.close()
    await redis.wait_closed()
