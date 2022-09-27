import uuid
from functools import lru_cache  # noqa: E999

from core.settings import settings
from db.cache_db import get_cache_db
from db.db import get_db, get_notify_pipeline
from extensions.tracer import _trace
from models import models
from pydantic import BaseModel
from pydantic.types import UUID4
from services.base_cache import BaseCacheStorage
from services.base_main import BaseMainStorage
from utils.utils import generate_password


class CacheUser(BaseModel):
    id: UUID4
    login: str
    email: str


class ConfirmID(BaseModel):
    _id: UUID4
    user_id: UUID4


class EventModel(BaseModel):
    user_id: UUID4


class UserService(BaseCacheStorage, BaseMainStorage):
    cache_model = CacheUser

    @_trace()
    def create_user(self, params: dict):
        user = self.create(
            need_commit=False,
            login=params['login'],
            email=params['email'],
            email_is_confirmed=params['email_is_confirmed']
        )
        user.set_password(params['password'])
        self.db.commit()
        return self.cache_model(**user.to_dict())

    @_trace()
    def get_users(
            self,
            page: int,
            per_page: int,
            base_url: str,
    ):
        query = self.get_query()

        cache_key = f'{base_url}?page={page}&per_page={per_page}'
        users = self.get_items_from_cache(cache_key=cache_key, model=self.cache_model)
        if not users:
            paginated_users = self.paginate(query=query, page=page, per_page=per_page)
            users = [self.cache_model(**user.to_dict()) for user in paginated_users.items]
            if users:
                self.put_items_to_cache(cache_key=cache_key, items=users)
        return {
            'items': users,
            'total': self.count(query),
            'page': page,
            'per_page': per_page,
        }

    @_trace()
    def get_user(self, user_id: str, base_url: str):
        cache_key = base_url

        user = self.get_one_item_from_cache(
            cache_key=cache_key,
            model=self.cache_model,
        )
        if not user:
            user_db = self.get(item_id=user_id)
            if user_db:
                user = self.cache_model(**user_db.to_dict())
                self.put_one_item_to_cache(cache_key=cache_key, item=user)
        return user

    @_trace()
    def update_password(self, user_id: str, password: str):
        user_db = self.get(item_id=user_id)
        user_db.set_password(password)
        self.db.commit()

    @_trace()
    def generate_password(self, user_id: str):
        password = generate_password()
        self.get(item_id=user_id).set_password(password)
        return password

    @_trace()
    def create_confirm_id(self, user_id: str) -> str:
        key = str(uuid.uuid4())
        self.put_one_item_to_cache(cache_key=key, item=ConfirmID(_id=key, user_id=user_id), expire=600)
        return key

    @_trace()
    def confirm_email(self, confirm_id: str) -> bool:
        item = self.get_one_item_from_cache(cache_key=confirm_id, model=ConfirmID)
        if not item:
            return False
        user = self.get(item_id=item.user_id)
        user.email_is_confirmed = True
        return True

    @_trace()
    def get_event_model(self, user_id: str, **kwargs):
        return EventModel(user_id=user_id, **kwargs)

    @_trace()
    def generate_password_event(self, user_id: str):
        notify_pipeline = get_notify_pipeline()

        key = str(uuid.uuid4()).encode('utf-8')

        value = self.get_event_model(user_id=user_id).json().encode('utf-8')

        notify_pipeline.send(topic=settings.GENERATE_PASSWORD_TOPIC, key=key, value=value)

    @_trace()
    def confirm_email_event(self, user_id: str):
        notify_pipeline = get_notify_pipeline()

        key = str(uuid.uuid4()).encode('utf-8')

        value = self.get_event_model(user_id=user_id).json().encode('utf-8')

        notify_pipeline.send(topic=settings.EMAIL_CONFIRMATION_TOPIC, key=key, value=value)


@lru_cache()
def get_user_service() -> UserService:
    user_service = UserService(
        cache=get_cache_db(),
        db=get_db(),
        db_model=models.User,
    )
    return user_service
