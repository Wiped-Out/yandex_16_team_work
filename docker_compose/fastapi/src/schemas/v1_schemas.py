from pydantic import BaseModel
from pydantic.types import UUID4
from models import genre, person
from typing import Optional


class FilmPage(BaseModel):
    title: str
    imdb_rating: Optional[float] = 0.01
    description: str
    genres: Optional[list[genre.Genre]]
    actors: Optional[list[person.Person]]
    screenwriters: Optional[list[person.Person]]
    director: Optional[person.Person]


class FilmMainPage(BaseModel):
    id: UUID4
    title: str
    imdb_rating: Optional[float] = 0.01
