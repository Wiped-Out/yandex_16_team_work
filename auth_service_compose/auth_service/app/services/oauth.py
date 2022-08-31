from functools import lru_cache

from db.cache_db import get_cache_db
from db.db import get_db
from extensions.tracer import _trace
from models import models
from models.models import OAuthEnum
from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage


class OauthService(BaseCacheStorage, BaseMainStorage):
    cache_model = None

    @_trace()
    def get_oauth(self, sub: str, type: OAuthEnum) -> models.Oauth:
        return self.filter_by(sub=sub, type=type, _first=True)

    @_trace()
    def create_oauth(self, params: dict):
        self.create(**params)


@lru_cache()
def get_oauth_service() -> OauthService:
    oauth_service = OauthService(
        cache=get_cache_db(),
        db=get_db(),
        db_model=models.Oauth,
    )
    return oauth_service
