from typing import List

from pydantic import UUID4, Field

from models.base import BaseOrjsonModel


class FilmBookmark(BaseOrjsonModel):
    user_id: UUID4
    film_id: UUID4


class FilmLike(BaseOrjsonModel):
    user_id: UUID4
    film_id: UUID4


class FilmProgress(BaseOrjsonModel):
    user_id: UUID4
    film_id: UUID4
    stamp: int


class UserComment(BaseOrjsonModel):
    user_id: UUID4
    film_id: UUID4
    comment: str
    created_at: int


class UserReview(BaseOrjsonModel):
    user_id: UUID4
    film_id: UUID4
    text: str
    created_at: int
    likes: List[UUID4] = Field(default=[])
    dislikes: List[UUID4] = Field(default=[])
