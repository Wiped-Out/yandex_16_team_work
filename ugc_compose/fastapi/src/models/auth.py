from pydantic import UUID4

from models.base import BaseOrjsonModel


class AuthUser(BaseOrjsonModel):
    highest_role: int = 0
    uuid: UUID4
