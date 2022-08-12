from functools import lru_cache
from pydantic import UUID4


class LikesService:
    async def give_like(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        # todo
        pass


@lru_cache()
def get_likes_service():
    return LikesService()
