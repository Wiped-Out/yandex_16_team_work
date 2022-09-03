import time
import uuid
from functools import lru_cache

from db.secondary_db import get_db
from fastapi import Depends
from models.models import UserReview

from services.secondary_db import AbstractSecondaryStorage, SecondaryStorage


class ReviewsService(SecondaryStorage):
    async def add_review(
            self,
            user_id: uuid.uuid4,
            film_id: uuid.uuid4,
            text: str,
    ) -> str:
        user_review = UserReview(
            user_id=user_id,
            film_id=film_id,
            text=text,
            created_at=int(time.time()),
        )

        return await self.create(collection='reviews', item=user_review)

    async def add_reaction(
            self,
            user_id: uuid.uuid4,
            review_id: str,
            reaction: str
    ):
        if reaction in ('like', 'dislike'):
            reaction_field = reaction + 's'
            await self.update(
                collection='reviews',
                id=review_id,
                update_field=reaction_field,
                data=user_id
            )


@lru_cache()
def get_reviews_service(
        secondary_db: AbstractSecondaryStorage = Depends(get_db),
):
    return ReviewsService(db=secondary_db)  # type: ignore
