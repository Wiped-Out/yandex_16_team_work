import orjson
from pydantic import BaseModel
from pydantic.types import UUID4
from utils import utils
from models.genre import Genre
from models.actor import Actor
from models.director import Director
from models.screenwriter import Screenwriter
from typing import Optional


class Film(BaseModel):
    id: UUID4
    title: str
    description: Optional[str]

    imdb_rating: float

    genres: list[Genre]

    actors: list[Actor]
    screenwriters: list[Screenwriter]
    director: Director

    actors_names: list[str]
    screenwriters_names: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
