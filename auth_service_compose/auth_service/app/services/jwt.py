from datetime import timedelta, timezone, datetime
from functools import lru_cache
from typing import Optional

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import BaseModel

from db.cache_db import get_cache_db
from db.db import get_db
from models import models
from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from services.refresh_token import get_refresh_token_service
from extensions.tracer import _trace


class Token(BaseModel):
    jti: str


class JWTService(BaseCacheStorage, BaseMainStorage):
    cache_model = Token
    db_model = models.RefreshToken

    @_trace()
    def create_access_token(self, user,
                            additional_claims: Optional[dict] = None) -> str:
        return create_access_token(identity=user,
                                   additional_claims=additional_claims,
                                   fresh=True)

    @_trace()
    def create_refresh_token(self, user) -> str:
        token = create_refresh_token(identity=user)
        refresh_token_service = get_refresh_token_service()
        refresh_token_service.create_refresh_token(
            params={"user_id": user.id,
                    "token": token,
                    "from_": datetime.now(timezone.utc),
                    "to": datetime.now(timezone.utc) + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
                    }
        )
        return token

    @_trace()
    def block_token(self, cache_key: str, expire: timedelta):

        self.put_one_item_to_cache(cache_key=cache_key,
                                   item=self.cache_model(jti=cache_key),
                                   expire=expire)

    @_trace()
    def get_blocked_token(self, cache_key: str):
        return self.get_one_item_from_cache(cache_key=cache_key,
                                            model=self.cache_model)


@lru_cache()
def get_jwt_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> JWTService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    jwt_service = JWTService(
        cache=cache,
        db=main_db,
        db_model=models.RefreshToken,
    )
    return jwt_service
