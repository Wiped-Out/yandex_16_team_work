from pydantic import BaseModel, Field
from pydantic.types import UUID4
import orjson
from utils import utils


class Genre(BaseModel):
    uuid: UUID4 = Field(alias="id")
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
