from functools import lru_cache
from pydantic import UUID4
from db.kafka import producer


class BookmarksService:
    async def add_bookmark(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        producer.send(
            topic="bookmarks",
            value=b"added to watch later",
            key=f"{user_id}+{film_id}".encode("UTF-8")
        )


@lru_cache()
def get_bookmarks_service():
    return BookmarksService()
