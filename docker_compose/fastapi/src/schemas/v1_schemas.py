from pydantic import BaseModel
from pydantic.types import UUID4
from typing import Optional


class Genre(BaseModel):
    uuid: UUID4
    name: str


class Person(BaseModel):
    uuid: UUID4
    full_name: str
    role: str
    film_ids: list[UUID4]


class Film(BaseModel):
    uuid: UUID4
    title: str
    imdb_raring: float


class FilmMainPage(BaseModel):
    id: UUID4
    title: str
    imdb_rating: Optional[float] = 0.01
