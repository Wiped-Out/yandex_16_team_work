from functools import lru_cache
from pydantic import UUID4


class FilmProgressService:
    async def save_film_progress(
            self,
            user_id: UUID4,
            film_id: UUID4,
            seconds: int
    ):
        # todo
        pass


@lru_cache()
def get_film_progress_service():
    return FilmProgressService()
