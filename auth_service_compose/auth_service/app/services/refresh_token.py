from datetime import datetime
from functools import lru_cache

from pydantic import UUID4, BaseModel

from db.cache_db import get_cache_db
from db.db import get_db
from models import models
from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage


class CacheRefreshToken(BaseModel):
    id: UUID4
    user_id: UUID4
    token: str
    from_: datetime
    to: datetime


class RefreshTokenService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheRefreshToken
    db_model = models.RefreshToken

    def get_refresh_tokens(self, user_id: str) -> list[cache_model]:
        db_refresh_tokens = self.filter_by(user_id=user_id, sort_by='to')
        return [self.cache_model(**refresh_token.to_dict()) for refresh_token in db_refresh_tokens]

    def create_refresh_token(self, params: dict) -> cache_model:
        refresh_token = self.create(**params)
        return self.cache_model(**refresh_token.to_dict())


@lru_cache()
def get_refresh_token_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> RefreshTokenService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    refresh_token_service = RefreshTokenService(
        cache=cache,
        db=main_db,
        db_model=models.RefreshToken,
    )
    return refresh_token_service
