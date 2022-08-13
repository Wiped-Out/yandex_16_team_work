import time
from functools import lru_cache
from pydantic import UUID4
from json import dumps
from services.main_db import AbstractMainStorage, MainStorage
from fastapi import Depends
from db.db import get_db


class FilmProgressService(MainStorage):
    async def save_film_progress(
            self,
            user_id: UUID4,
            film_id: UUID4,
            seconds: int
    ):
        value = {"user_id": user_id,
                 "film_id": film_id,
                 "seconds": seconds,
                 "stamp": int(time.time()),
                 }

        self.send(
            topic="film_progress",
            value=dumps(value).encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache()
def get_film_progress_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return FilmProgressService(db=main_db)
