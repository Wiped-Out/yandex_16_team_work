from typing import List, Optional

from models.base import BaseOrjsonModel
from pydantic import BaseModel
from pydantic.types import UUID4


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

    genre: List[GenreInFilm]

    actors: List[PersonInFilm]
    writers: List[PersonInFilm]
    directors: List[PersonInFilm]

    actors_names: List[str]
    writers_names: List[str]
    directors_names: List[str]
