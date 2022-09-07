from datetime import datetime

from pydantic import UUID4, BaseModel


class FilmLike(BaseModel):
    user_id: str
    film_id: str
    rating: int


class FilmBookmark(BaseModel):
    user_id: str
    film_id: str


class UserReview(BaseModel):
    user_id: str
    film_id: str
    text: str
    created_at: datetime
