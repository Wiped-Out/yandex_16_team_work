import asyncio
import json
import random
import time
from typing import List

import asyncpg
from config import settings

dsl = {
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT,
    'user': settings.POSTGRES_USER,
    'database': settings.POSTGRES_DB,
    'password': settings.POSTGRES_PASSWORD,
}


def get_user_ids(n: int) -> List[str]:
    result = []
    with open('data/users.json', encoding='utf-8') as file:
        data = json.load(file)
        result = random.choices(data, k=n)
    return result


def get_film_ids(n: int) -> List[str]:
    result = []
    with open('data/films.json', encoding='utf-8') as file:
        data = json.load(file)
        result = random.choices(data, k=n)
    return result


async def get_user_likes(pool: asyncpg.pool.Pool, user_id: str) -> List[asyncpg.Record]:
    sql = "SELECT film_id FROM test_data.film_like WHERE user_id = '{user_id}'"
    return await pool.fetch(sql.format(user_id=user_id))


async def get_user_bookmarks(pool: asyncpg.pool.Pool, user_id: str) -> List[asyncpg.Record]:
    sql = "SELECT film_id FROM test_data.film_bookmark WHERE user_id = '{user_id}'"
    return await pool.fetch(sql.format(user_id=user_id))


async def get_film_rating(pool: asyncpg.pool.Pool, film_id: str) -> List[asyncpg.Record]:
    sql = "SELECT AVG(rating) from test_data.film_like WHERE film_id = '{film_id}'"
    return await pool.fetch(sql.format(film_id=film_id))


async def main():
    pool = await asyncpg.create_pool(**dsl)
    tasks = []
    users = get_user_ids(100)
    films = get_film_ids(100)
    for user in users:
        tasks.append(asyncio.create_task(get_user_likes(pool, user)))
        tasks.append(asyncio.create_task(get_user_bookmarks(pool, user)))
    for film in films:
        tasks.append(asyncio.create_task(get_film_rating(pool, film)))
    await asyncio.gather(*tasks)
    await pool.close()

if __name__ == '__main__':
    start = time.monotonic()
    asyncio.run(main())
    end = time.monotonic()
    print(end - start)
