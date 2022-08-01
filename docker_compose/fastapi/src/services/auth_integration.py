from functools import lru_cache

from fastapi import Depends, HTTPException

from core.config import settings
from db.cache_db import get_cache_db
from models.auth import AuthUser
from services.base import AsyncCacheStorage
from services.base_cache import BaseCacheStorage
from services.base_request import BaseRequest
from utils.utils import decode_jwt


class AuthService(BaseCacheStorage, BaseRequest):

    async def auth_user(self, Authorization: str):
        try:
            user = await self.get_one_item_from_cache(cache_key=Authorization, model=AuthUser)
            if user:
                return user
            exp_time = 300
            decoded_jwt = decode_jwt(token=Authorization)
            try:
                response = await self.get(
                    url=f"{settings.AUTH_SERVICE_URL}/users/{decoded_jwt['sub']}/role/highest_role",
                    headers={"Authorization": f"Bearer {Authorization}"})
                user = AuthUser(highest_role=response.body['level'], uuid=decoded_jwt['sub'])
            except ConnectionError:
                user = AuthUser(highest_role=0, uuid=decoded_jwt['sub'])
                exp_time = 60
            await self.put_one_item_to_cache(cache_key=Authorization, item=user, expire=exp_time)
            return user
        except AttributeError as e:
            raise HTTPException(status_code=404, detail=response['msg']) from e


@lru_cache()
def get_auth_service(
        cache: AsyncCacheStorage = Depends(get_cache_db),
) -> AuthService:
    return AuthService(cache=cache)
