import asyncio
import json
import random
import time
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import settings

MONGODB_URL = f'mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}'


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


async def get_user_likes(db: AsyncIOMotorDatabase, user_id: str) -> List[str]:
    # return [like['film_id'] async for like in db.likes.find({'user_id': user_id}, {'film_id': 1})]
    return await db.likes.find({'user_id': user_id}, {'film_id': 1}).to_list(length=None)


async def get_user_bookmarks(db: AsyncIOMotorDatabase, user_id: str) -> List[str]:
    return [bookmark['film_id'] async for bookmark in db.bookmarks.find({'user_id': user_id})]


async def get_film_rating(db: AsyncIOMotorDatabase, film_id: str):
    pipeline = [
        {
            "$match": {
                "film_id": film_id,
            }
        },
        {
            "$group": {
                "_id": "Avarage rating",
                "avg": {"$avg": "$rating"}
            }
        }
    ]
    return await db.likes.aggregate(pipeline).to_list(length=None)


async def main(db: AsyncIOMotorDatabase):
    tasks = []
    users = get_user_ids(100)
    films = get_film_ids(100)
    for user in users:
        tasks.append(asyncio.create_task(get_user_likes(db, user)))
        tasks.append(asyncio.create_task(get_user_bookmarks(db, user)))
    for film in films:
        tasks.append(asyncio.create_task(get_film_rating(db, film)))
    await asyncio.wait(tasks)

if __name__ == '__main__':
    start = time.monotonic()
    client = AsyncIOMotorClient(MONGODB_URL, UuidRepresentation='standard')
    db = client.python_db
    asyncio.run(main(db))
    end = time.monotonic()
    print(end - start)
