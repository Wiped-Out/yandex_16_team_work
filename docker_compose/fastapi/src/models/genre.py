from pydantic import BaseModel, Field
from pydantic.types import UUID4
from models.base import BaseOrjsonModel


class Genre(BaseModel, BaseOrjsonModel):
    uuid: UUID4 = Field(alias="id")
    name: str

    class Config:
        allow_population_by_field_name = True
