from services.base_cache import BaseCacheStorage, CacheStorage
from services.base_main import BaseMainStorage, MainStorage
from models import models
from pydantic import BaseModel
from pydantic.types import UUID4
from db.cache_db import get_cache_db
from db.db import get_db
from functools import lru_cache


class CacheUser(BaseModel):
    id: UUID4
    login: str
    email: str


class UserService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheUser

    def create_user(self, params: dict) -> cache_model:
        user = self.create(
            need_commit=False,
            login=params["login"],
            email=params["email"],
        )
        user.set_password(params["password"])
        self.db.commit()
        return self.cache_model(**user.to_dict())

    def get_users(self, cache_key: str) -> list[cache_model]:
        users = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not users:
            db_users = self.get_all()
            users = [self.cache_model(**user.to_dict()) for user in db_users]
            if users:
                self.put_items_to_cache(cache_key=cache_key, items=users)
        return users

    def get_user(self, user_id: str, cache_key: str) -> cache_model:
        user = self.get_one_item_from_cache(
            cache_key=cache_key,
            model=self.cache_model,
        )
        if not user:
            user_db = self.get(item_id=user_id)
            user = self.cache_model(**user_db.to_dict())
            if user:
                self.put_one_item_to_cache(cache_key=cache_key, item=user)
        return user

    def update_password(self, user_id: str, password: str):
        user_db = self.get(item_id=user_id)
        user_db.set_password(password)
        self.db.commit()


@lru_cache()
def get_user_service(
        cache: CacheStorage = None,
        main_db: MainStorage = None
) -> UserService:
    cache: CacheStorage = get_cache_db() or cache
    main_db: MainStorage = get_db() or main_db
    user_service = UserService(
        cache=cache,
        db=main_db,
        db_model=models.User,
    )
    return user_service
