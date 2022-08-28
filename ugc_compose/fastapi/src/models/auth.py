from models.base import BaseOrjsonModel
from pydantic import UUID4


class AuthUser(BaseOrjsonModel):
    highest_role: int = 0
    uuid: UUID4
