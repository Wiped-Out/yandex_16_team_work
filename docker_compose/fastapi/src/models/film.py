import orjson
from pydantic import BaseModel
from pydantic.types import UUID4
from utils import utils
from models.genre import Genre
from typing import Optional
from models.person import Person


class Film(BaseModel):
    id: UUID4
    title: str
    description: Optional[str]

    imdb_rating: float

    genres: list[Genre]

    actors: list[Person]
    screenwriters: list[Person]
    director: Person

    actors_names: list[Person]
    screenwriters_names: list[Person]

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
