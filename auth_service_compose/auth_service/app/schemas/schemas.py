from pydantic import BaseModel
from pydantic.types import UUID4


class Role(BaseModel):
    id: UUID4
    name: str
    level: str
