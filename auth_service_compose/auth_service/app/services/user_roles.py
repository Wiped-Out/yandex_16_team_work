from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from models import models
from functools import lru_cache
from db.cache_db import get_cache_db
from db.db import get_db


class UserRolesService(BaseCacheStorage, BaseMainStorage):
    user_model = models.User
    role_model = models.Role

    def add_role_to_user(self, user_id: str, role_id: str):
        user = self.db.get(item_id=user_id, model=self.user_model)
        role = self.db.get(item_id=role_id, model=self.role_model)
        user.roles.append(role)
        role.users.append(user)
        self.db.add(user)
        self.db.add(role)
        self.db.commit()

    def delete_role_from_user(self, user_id: str, role_id: str):
        user = self.db.get(item_id=user_id, model=self.user_model)
        role = self.db.get(item_id=role_id, model=self.role_model)

        user.roles.remove(role)

        self.db.add(user)

        self.db.commit()


@lru_cache()
def get_user_roles_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> UserRolesService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    role_service = UserRolesService(
        cache=cache,
        db=main_db,
        db_model=models.User,
    )
    return role_service