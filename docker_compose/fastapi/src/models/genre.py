from pydantic import Field
from pydantic.types import UUID4
from models.base import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    uuid: UUID4 = Field(alias="id")
    name: str

    class Config:
        allow_population_by_field_name = True
