from functools import lru_cache

from models.auth import AuthUser
from utils.utils import decode_jwt


class AuthService:
    model = AuthUser

    async def auth_user(self, authorization: str):
        decoded_jwt = decode_jwt(token=authorization)

        user = self.model(highest_role=decoded_jwt["role"], uuid=decoded_jwt['sub'])
        return user


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
