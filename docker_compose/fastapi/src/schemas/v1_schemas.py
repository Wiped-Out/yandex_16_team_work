from pydantic import BaseModel
from pydantic.types import UUID4


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
