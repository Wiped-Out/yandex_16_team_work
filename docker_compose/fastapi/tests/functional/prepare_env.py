import asyncio

from utils.wait_for_redis import wait_for_redis
from utils.wait_for_es import wait_for_es
from utils.create_indexes_in_es import create_indexes_in_es
from utils.load_data_to_elastic import load_data_to_elastic

if __name__ == '__main__':
    scripts = (
        wait_for_redis,
        wait_for_es,
        create_indexes_in_es,
        load_data_to_elastic
    )

    loop = asyncio.get_event_loop()

    for script in scripts:
        loop.run_until_complete(script())
