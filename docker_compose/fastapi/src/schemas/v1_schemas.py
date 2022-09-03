from typing import List, Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Genre(BaseModel):
    uuid: UUID4
    name: str


class Person(BaseModel):
    uuid: UUID4
    full_name: str
    role: str
    film_ids: List[UUID4]


class FilmMainPage(BaseModel):
    id: UUID4
    title: str
    imdb_rating: Optional[float] = 0.01
