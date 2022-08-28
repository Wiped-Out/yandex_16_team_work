from enum import Enum

from models.base import BaseOrjsonModel
from pydantic import Field
from pydantic.types import UUID4


class PersonType(str, Enum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class Person(BaseOrjsonModel):
    uuid: UUID4 = Field(alias='id')
    full_name: str
    role: PersonType
    film_ids: list[UUID4]

    class Config:
        allow_population_by_field_name = True
