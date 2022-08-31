import time
from functools import lru_cache

from db.db import get_db
from fastapi import Depends
from models.models import UserComment
from pydantic import UUID4
from services.main_db import AbstractMainStorage, MainStorage


class CommentsService(MainStorage):
    async def add_comment(
            self,
            user_id: UUID4,
            film_id: UUID4,
            comment: str,
    ):
        user_comment = UserComment(
            user_id=user_id,
            film_id=film_id,
            comment=comment,
            created_at=int(time.time()),
        )

        key = '{user_id}+{film_id}'.format(user_id=user_id, film_id=film_id)
        self.send(
            topic='user_comments',
            value=user_comment.json().encode(),
            key=key.encode(),
        )


@lru_cache()
def get_comments_service(
        main_db: AbstractMainStorage = Depends(get_db),
):
    return CommentsService(db=main_db)  # type: ignore
