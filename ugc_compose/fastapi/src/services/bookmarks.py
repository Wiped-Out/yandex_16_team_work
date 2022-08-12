from functools import lru_cache
from pydantic import UUID4


class BookmarksService:
    async def add_bookmark(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        # todo
        pass


@lru_cache()
def get_bookmarks_service():
    return BookmarksService()
