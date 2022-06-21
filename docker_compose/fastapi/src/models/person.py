import orjson
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from utils import utils
from enum import Enum


class PersonType(str, Enum):
    actor = "actor"
    director = "director"
    writer = "writer"


class Person(BaseModel):
    uuid: UUID4 = Field(alias="id")
    full_name: str
    role: PersonType
    film_ids: list[UUID4]

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
        allow_population_by_field_name = True
