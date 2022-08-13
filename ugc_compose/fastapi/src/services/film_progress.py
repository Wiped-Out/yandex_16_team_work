from functools import lru_cache
from pydantic import UUID4
from db.kafka import producer


class FilmProgressService:
    async def save_film_progress(
            self,
            user_id: UUID4,
            film_id: UUID4,
            seconds: int
    ):
        producer.send(
            topic="film_progress",
            value=str(seconds).encode("UTF-8"),
            key=f"{user_id}+{film_id}".encode("UTF-8"),
        )


@lru_cache()
def get_film_progress_service():
    return FilmProgressService()
