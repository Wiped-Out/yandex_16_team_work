from datetime import datetime  # noqa: E999
from functools import lru_cache

from db.cache_db import get_cache_db
from db.db import get_db
from extensions.tracer import _trace
from models import models
from pydantic import BaseModel
from pydantic.types import UUID4
from services.base_cache import BaseCacheStorage
from services.base_main import BaseMainStorage


class CacheLog(BaseModel):
    id: UUID4
    device: str
    action: str
    method: str
    when: datetime


class LogsService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheLog

    @_trace()
    def create_log(self, **params):
        log = self.create(**params)
        return self.cache_model(**log.to_dict())

    @_trace()
    def get_logs(
            self,
            user_id: str,
            page: int,
            per_page: int,
            base_url: str,
            **kwargs,
    ):

        query = self.filter_by(user_id=user_id, **kwargs)

        cache_key = f'{base_url}?page={page}&per_page={per_page}'
        history = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not history:
            paginated_answer = self.paginate(query=query, page=page, per_page=per_page)

            history = [self.cache_model(**h.to_dict()) for h in paginated_answer.items]
            if history:
                self.put_items_to_cache(cache_key=cache_key, items=history)

        return {'items': history, 'total': self.count(query), 'page': page, 'per_page': per_page}


@lru_cache()
def get_logs_service() -> LogsService:
    logs_service = LogsService(
        cache=get_cache_db(),
        db=get_db(),
        db_model=models.Log,
    )
    return logs_service
