from functools import lru_cache

from models.auth import AuthUser
from services.base_request import BaseRequest
from utils.utils import decode_jwt


class AuthService(BaseRequest):
    model = AuthUser

    async def auth_user(self, Authorization: str):
        decoded_jwt = decode_jwt(token=Authorization)

        user = self.model(highest_role=decoded_jwt["role"], uuid=decoded_jwt['sub'])
        return user


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
