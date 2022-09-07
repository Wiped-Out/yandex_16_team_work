import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import IO, Dict, List

import asyncpg

from config import settings

dsl = {
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT,
    'user': settings.POSTGRES_USER,
    'database': settings.POSTGRES_DB,
    'password': settings.POSTGRES_PASSWORD,
}


async def load_user_like(pool: asyncpg.pool.Pool, file: IO) -> None:
    data = [(str(uuid.uuid4()), item['user_id'], item['film_id'], item['rating'])
            for item in json.load(file)]
    await pool.executemany('''
        INSERT INTO test_data.film_like (id, user_id, film_id, rating)
        VALUES ($1, $2, $3, $4);
    ''', data)


async def load_user_bookmark(pool: asyncpg.pool.Pool, file: IO) -> None:
    data = [(str(uuid.uuid4()), item['user_id'], item['film_id'])
            for item in json.load(file)]
    await pool.executemany('''
        INSERT INTO test_data.film_bookmark (id, user_id, film_id)
        VALUES ($1, $2, $3);
    ''', data)


async def load_user_review(pool: asyncpg.pool.Pool, file: IO) -> None:
    data = [
        (
            str(uuid.uuid4()),
            item['user_id'],
            item['film_id'],
            item['text'],
            datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S')
        )
        for item in json.load(file)
    ]
    await pool.executemany('''
        INSERT INTO test_data.user_review (id, user_id, film_id, text, created_at)
        VALUES ($1, $2, $3, $4, $5);
    ''', data)


async def main():
    pool = await asyncpg.create_pool(**dsl)
    tasks = []
    likes_file = open('data/likes.json', encoding='utf-8')
    bookmarks_file = open('data/bookmarks.json', encoding='utf-8')
    reviews_file = open('data/reviews.json', encoding='utf-8')

    tasks.append(asyncio.create_task(load_user_like(pool, likes_file)))
    tasks.append(asyncio.create_task(load_user_bookmark(pool, bookmarks_file)))
    tasks.append(asyncio.create_task(load_user_review(pool, reviews_file)))

    for task in tasks:
        await task

    likes_file.close()
    bookmarks_file.close()
    reviews_file.close()


if __name__ == "__main__":
    start = time.monotonic()
    asyncio.run(main())
    end = time.monotonic()
    print(end - start)
