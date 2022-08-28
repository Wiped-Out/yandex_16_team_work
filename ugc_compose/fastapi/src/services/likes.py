from functools import lru_cache

from db.db import get_db
from fastapi import Depends
from models.models import FilmLike
from pydantic import UUID4
from services.main_db import AbstractMainStorage, MainStorage


class LikesService(MainStorage):
    async def give_like(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        film_like = FilmLike(user_id=user_id, film_id=film_id)
        self.send(
            topic='film_likes',
            value=film_like.json().encode(),
            key=f'{user_id}+{film_id}'.encode(),
        )


@lru_cache()
def get_likes_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return LikesService(db=main_db)
