from functools import lru_cache
from pydantic import UUID4


class CommentsService:
    async def add_comment(
            self,
            user_id: UUID4,
            film_id: UUID4,
            comment: str
    ):
        # todo
        pass


@lru_cache()
def get_comments_service():
    return CommentsService()
