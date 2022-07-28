from datetime import datetime
from functools import lru_cache

from pydantic import BaseModel
from pydantic.types import UUID4

from db.cache_db import get_cache_db
from db.db import get_db
from models import models
from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage


class CacheLog(BaseModel):
    id: UUID4
    device: str
    action: str
    method: str
    when: datetime


class LogsService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheLog

    def create_log(self, **params) -> cache_model:
        log = self.create(**params)
        return self.cache_model(**log.to_dict())

    def get_logs(
            self,
            cache_key: str,
            user_id: str,
            page: int,
            per_page: int,
            **kwargs
    ):
        query = self.filter_by(user_id=user_id, **kwargs)

        history = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not history:
            paginated_answer = self.paginate(query=query, page=page, per_page=per_page)

            history = [self.cache_model(**h.to_dict()) for h in paginated_answer.items]
            if history:
                self.put_items_to_cache(cache_key=cache_key, items=history)

        return {"items": history, "total": self.count(query), "page": page, "per_page": per_page}


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
