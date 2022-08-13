from functools import lru_cache
from pydantic import UUID4
from db.kafka import producer


class LikesService:
    async def give_like(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        producer.send(
            topic="likes",
            value=b"like",
            key=f"{user_id}+{film_id}".encode("UTF-8"),
        )


@lru_cache()
def get_likes_service():
    return LikesService()
