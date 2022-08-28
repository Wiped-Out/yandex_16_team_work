from functools import lru_cache

from db.db import get_db
from fastapi import Depends
from models.models import FilmProgress
from pydantic import UUID4
from services.main_db import AbstractMainStorage, MainStorage


class FilmProgressService(MainStorage):
    async def save_film_progress(
            self,
            user_id: UUID4,
            film_id: UUID4,
            stamp: int,
    ):
        film_progress = FilmProgress(
            user_id=user_id,
            film_id=film_id,
            stamp=stamp,
        )

        self.send(
            topic='film_progress',
            value=film_progress.json().encode(),
            key=f'{user_id}+{film_id}'.encode(),
        )


@lru_cache()
def get_film_progress_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return FilmProgressService(db=main_db)
