import asyncio

from utils.wait_for_redis import wait_for_redis
from utils.wait_for_es import wait_for_es

if __name__ == '__main__':
    scripts = (
        wait_for_redis,
        wait_for_es,
    )

    loop = asyncio.get_event_loop()

    for script in scripts:
        loop.run_until_complete(script())
