from functools import lru_cache
from json import dumps

from fastapi import Depends
from pydantic import UUID4

from db.db import get_db
from models.models import FilmBookmark
from services.main_db import AbstractMainStorage, MainStorage


class BookmarksService(MainStorage):
    async def add_bookmark(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        film_bookmark = FilmBookmark(user_id=user_id, film_id=film_id)
        self.send(
            topic="film_bookmarks",
            value=film_bookmark.json().encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache()
def get_bookmarks_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return BookmarksService(db=main_db)
