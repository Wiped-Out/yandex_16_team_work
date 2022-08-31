from datetime import datetime
from functools import lru_cache

from db.cache_db import get_cache_db
from db.db import get_db
from extensions.tracer import _trace
from models import models
from pydantic import UUID4, BaseModel
from services.base_cache import BaseCacheStorage
from services.base_main import BaseMainStorage


class CacheRefreshToken(BaseModel):
    id: UUID4
    user_id: UUID4
    token: str
    from_: datetime
    to: datetime


class RefreshTokenService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheRefreshToken
    db_model = models.RefreshToken

    @_trace()
    def get_refresh_tokens(self, user_id: str):
        db_refresh_tokens = self.filter_by(user_id=user_id, sort_by='to')
        return [self.cache_model(**refresh_token.to_dict()) for refresh_token in db_refresh_tokens]

    @_trace()
    def create_refresh_token(self, params: dict):
        refresh_token = self.create(**params)
        return self.cache_model(**refresh_token.to_dict())


@lru_cache()
def get_refresh_token_service(
) -> RefreshTokenService:
    refresh_token_service = RefreshTokenService(
        cache=get_cache_db(),
        db=get_db(),
        db_model=models.RefreshToken,
    )
    return refresh_token_service
