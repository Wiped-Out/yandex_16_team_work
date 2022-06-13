from pydantic import BaseModel
from pydantic.types import UUID4
import orjson
from utils import utils


class Genre(BaseModel):
    id: UUID4
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
