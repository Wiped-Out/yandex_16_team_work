from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from models import models
from db.cache_db import get_cache_db
from db.db import get_db
from pydantic import BaseModel
from pydantic.types import UUID4


class CacheRole(BaseModel):
    id: UUID4
    name: str
    level: int


class RoleService(BaseCacheStorage, BaseMainStorage):
    db_model = models.Role
    cache_model = CacheRole

    def get_roles(self, cache_key: str) -> list[cache_model]:
        roles = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not roles:
            db_roles = self.db_model.query.all()
            roles = [self.cache_model(**role.to_dict()) for role in db_roles]
            if roles:
                self.put_items_to_cache(cache_key=cache_key, items=roles)
        return roles

    def get_role(self, role_id: str, cache_key: str) -> cache_model:
        role = self.get_one_item_from_cache(cache_key=cache_key, model=self.cache_model)
        if not role:
            db_role = self.db_model.query.filter(self.db_model.id == role_id).first()
            role = self.cache_model(**db_role.to_dict())
            if role:
                self.put_one_item_to_cache(cache_key=cache_key, item=role)
        return role

    def update_role(self, role_id: str, body: dict):
        # todo
        pass

    def create_role(self, body: dict):
        # todo
        pass

    def delete_role(self, role_id: str):
        # todo
        pass


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
