import orjson
from pydantic import BaseModel

from utils import utils


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
