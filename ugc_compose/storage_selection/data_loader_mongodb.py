import json
import time

import pymongo
from config import settings

MONGODB_URL = f'mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}'


def insert_to_collection(db: pymongo.database.Database, json_file: str, collection: str) -> None:
    with open(json_file, encoding='utf-8') as file:
        data = json.load(file)
        db.get_collection(collection).insert_many(data)


def load_data(db: pymongo.database.Database) -> None:
    insert_to_collection(db, 'data/likes.json', 'likes')
    insert_to_collection(db, 'data/bookmarks.json', 'bookmarks')
    insert_to_collection(db, 'data/reviews.json', 'reviews')


def main() -> None:
    client = pymongo.MongoClient(MONGODB_URL, UuidRepresentation='standard')
    load_data(client.python_db)


if __name__ == "__main__":
    start = time.monotonic()
    main()
    end = time.monotonic()
    print(end - start)
