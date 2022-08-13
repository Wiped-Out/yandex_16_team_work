from functools import lru_cache
from pydantic import UUID4
from json import dumps
from services.main_db import AbstractMainStorage, MainStorage
from fastapi import Depends
from db.db import get_db


class BookmarksService(MainStorage):
    async def add_bookmark(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        self.send(
            topic="film_bookmarks",
            value=dumps({"user_id": user_id, "film_id": film_id}).encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache()
def get_bookmarks_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return BookmarksService(db=main_db)
