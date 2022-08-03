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
        oauth = self.create(**params)


@lru_cache()
def get_oauth_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> OauthService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    oauth_service = OauthService(
        cache=cache,
        db=main_db,
        db_model=models.Oauth,
    )
    return oauth_service
