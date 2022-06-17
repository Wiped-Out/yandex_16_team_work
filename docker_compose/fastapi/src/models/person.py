import orjson
from pydantic import BaseModel
from pydantic.types import UUID4
from utils import utils
from enum import Enum


class PersonType(str, Enum):
    actor = "actor"
    director = "director"
    writer = "writer"


class Person(BaseModel):
    id: UUID4
    full_name: str
    role: PersonType

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
