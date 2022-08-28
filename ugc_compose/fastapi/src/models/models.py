from models.base import BaseOrjsonModel
from pydantic import UUID4


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
