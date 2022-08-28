from functools import lru_cache

from db.cache_db import get_cache_db
from fastapi import Depends
from models.auth import AuthUser
from services.base import AsyncCacheStorage
from services.base_cache import BaseCacheStorage
from utils.utils import decode_jwt


class AuthService(BaseCacheStorage):
    model = AuthUser

    async def auth_user(self, authorization: str):
        decoded_jwt = decode_jwt(token=authorization)

        user = self.model(highest_role=decoded_jwt['role'], uuid=decoded_jwt['sub'])
        return user


@lru_cache()
def get_auth_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
) -> AuthService:
    return AuthService(cache=cache)
