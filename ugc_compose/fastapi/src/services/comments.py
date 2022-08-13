from functools import lru_cache
from pydantic import UUID4
from db.kafka import producer


class CommentsService:
    async def add_comment(
            self,
            user_id: UUID4,
            film_id: UUID4,
            comment: str
    ):
        producer.send(
            topic="comments",
            value=comment.encode("UTF-8"),
            key=f"{user_id}+{film_id}".encode("UTF-8"),
        )


@lru_cache()
def get_comments_service():
    return CommentsService()
