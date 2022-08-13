import time
from functools import lru_cache
from pydantic import UUID4
from json import dumps
from services.main_db import AbstractMainStorage, MainStorage
from fastapi import Depends
from db.db import get_db


class CommentsService(MainStorage):
    async def add_comment(
            self,
            user_id: UUID4,
            film_id: UUID4,
            comment: str
    ):
        value = {"user_id": user_id,
                 "film_id": film_id,
                 "comment": comment,
                 "created_at": int(time.time()),
                 }

        self.send(
            topic="user_comments",
            value=dumps(value).encode(),
            key=f"{user_id}+{film_id}".encode(),
        )


@lru_cache()
def get_comments_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return CommentsService(db=main_db)
