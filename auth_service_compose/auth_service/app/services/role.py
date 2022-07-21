from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from models import models
from db.cache_db import get_cache_db
from db.db import get_db
from pydantic import BaseModel
from pydantic.types import UUID4
from functools import lru_cache


class CacheRole(BaseModel):
    id: UUID4
    name: str
    level: int


class RoleService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheRole

    def get_roles(
            self,
            cache_key: str,
            page: int,
            per_page: int,
    ):
        query = self.get_query()

        roles = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not roles:
            paginated_roles = self.paginate(query=query, page=page, per_page=per_page)
            roles = [self.cache_model(**role.to_dict()) for role in paginated_roles.items]
            if roles:
                self.put_items_to_cache(cache_key=cache_key, items=roles)

        return {
            "items": roles,
            "total": self.count(query),
            "page": page,
            "per_page": per_page
        }

    def get_role(self, role_id: str, cache_key: str) -> cache_model:
        role = self.get_one_item_from_cache(cache_key=cache_key, model=self.cache_model)
        if not role:
            db_role = self.get(item_id=role_id)
            role = self.cache_model(**db_role.to_dict())
            if role:
                self.put_one_item_to_cache(cache_key=cache_key, item=role)
        return role

    def update_role(self, role_id: str, params: dict):
        self.update(item_id=role_id, **params)

    def create_role(self, params: dict) -> cache_model:
        role = self.create(**params)
        return self.cache_model(**role.to_dict())


@lru_cache()
def get_role_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> RoleService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    role_service = RoleService(
        cache=cache,
        db=main_db,
        db_model=models.Role,
    )
    return role_service
