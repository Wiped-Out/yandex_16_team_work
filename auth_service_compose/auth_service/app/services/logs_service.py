import re
from datetime import datetime
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from db.cache_db import get_cache_db
from db.db import get_db
from models import models
from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from services.user import get_user_service


class CacheLog(BaseModel):
    id: UUID4
    device: str
    action: str
    when: datetime


class LogsService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheLog

    def create_log(self, **params) -> cache_model:
        log = self.create(**params)
        return self.cache_model(**log.to_dict())

    def get_logs(self, cache_key: str, user_id: str, pattern: Optional[str] = None) -> cache_model:
        history = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not history:
            user_service = get_user_service()
            user_db = user_service.get(item_id=user_id)

            history = self._get_logs_by_pattern(user_db=user_db, pattern=pattern)
            history = [self.cache_model(**h.to_dict()) for h in history]
            if history:
                self.put_items_to_cache(cache_key=cache_key, items=history)
        return history

    def _get_logs_by_pattern(self, user_db, pattern: Optional[str] = None):
        return [log for log in user_db.logs if re.search(pattern, log.action)] if pattern else user_db.logs


@lru_cache()
def get_logs_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> LogsService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    logs_service = LogsService(
        cache=cache,
        db=main_db,
        db_model=models.Log,
    )
    return logs_service
