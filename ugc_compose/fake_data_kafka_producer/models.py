from datetime import datetime

from pydantic import UUID4, BaseModel


class FilmLike(BaseModel):
    user_id: UUID4
    film_id: UUID4


class FilmBookmark(BaseModel):
    user_id: UUID4
    film_id: UUID4


class FilmProgress(BaseModel):
    user_id: UUID4
    film_id: UUID4
    timestamp: int


class UserComment(BaseModel):
    user_id: UUID4
    film_id: UUID4
    comment: str
    created_at: datetime
