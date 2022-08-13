from functools import lru_cache
from pydantic import UUID4
from json import dumps
from services.main_db import AbstractMainStorage, MainStorage
from fastapi import Depends
from db.db import get_db


class LikesService(MainStorage):
    async def give_like(
            self,
            user_id: UUID4,
            film_id: UUID4,
    ):
        self.send(
            topic="film_likes",
            value=dumps({"user_id": user_id, "film_id": film_id}).encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache()
def get_likes_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return LikesService(db=main_db)
