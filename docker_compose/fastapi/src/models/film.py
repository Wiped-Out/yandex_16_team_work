from pydantic import BaseModel
from pydantic.types import UUID4
from typing import Optional
from models.base import BaseOrjsonModel


class PersonInFilm(BaseModel):
    id: UUID4
    full_name: str


class GenreInFilm(BaseModel):
    id: UUID4
    name: str


class Film(BaseOrjsonModel):
    id: UUID4
    title: str
    description: Optional[str]

    imdb_rating: float

    genre: list[GenreInFilm]

    actors: list[PersonInFilm]
    writers: list[PersonInFilm]
    directors: list[PersonInFilm]

    actors_names: list[str]
    writers_names: list[str]
    directors_names: list[str]
