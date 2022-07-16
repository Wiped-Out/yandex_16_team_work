from datetime import datetime

from pydantic import BaseModel
from pydantic.types import UUID4


class Role(BaseModel):
    id: UUID4
    name: str
    level: str


class User(BaseModel):
    id: UUID4
    login: str
    email: str


class LoginHistory(BaseModel):
    id: UUID4
    device: str
    when: datetime


class JWT(BaseModel):
    access_token: str
    refresh_token: str


class JWTRefresh(BaseModel):
    access_token: str
