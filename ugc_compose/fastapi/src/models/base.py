from pydantic import BaseModel
import orjson
from utils import utils


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = utils.orjson_dumps
