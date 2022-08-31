from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from typing import Optional

from extensions.tracer import _trace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query


class AdditionalActions(str, Enum):
    _sort_by = '_sort_by'
    _first = '_first'


def sqlalchemy_additional_actions():
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            actions = {item.value: kwargs.pop(item.value) if item.value in kwargs and item.value else None  # noqa: E501
                       for item in AdditionalActions}
            result: Query = func(*args, **kwargs)
            model = kwargs['model']

            # Сортировка
            if value := actions[AdditionalActions._sort_by]:
                if value.startswith('-'):
                    result.order_by(getattr(model, value).desc())
                else:
                    result.order_by(getattr(model, value))

            # Если необходимо получить один элемент
            if actions[AdditionalActions._first]:
                result = result.first()
            return result

        return inner

    return func_wrapper


class MainStorage(ABC):
    @abstractmethod
    def get(self, item_id: str, model, **kwargs):
        pass

    @abstractmethod
    def create(self, model, need_commit: bool = True, **kwargs):
        pass

    @abstractmethod
    def update(self, item_id: str, model, **kwargs):
        pass

    @abstractmethod
    def commit(self, **kwargs):
        pass

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, item_id: str, model, **kwargs):
        pass

    @abstractmethod
    def get_all(self, **kwargs):
        pass

    @abstractmethod
    def filter_by(self, **kwargs):
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass

    @abstractmethod
    def paginate(self, query: Query, page: int, per_page: int, **kwargs):
        pass

    @abstractmethod
    def count(self, query: Query, **kwargs):
        pass

    @abstractmethod
    def like(self, model, query: Query, field, pattern: str, **kwargs):
        pass

    @abstractmethod
    def get_query(self, *args, **kwargs):
        pass


class BaseSQLAlchemyStorage(MainStorage):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get(self, item_id: str, model, **kwargs):
        return model.query.get(item_id)

    def create(self, model, need_commit: bool = True, **kwargs):
        item = model(**kwargs)
        self.add(item)

        if need_commit:
            self.commit()
        return item

    def update(self, item_id: str, model, **kwargs):
        model.query.filter_by(id=item_id).update(kwargs)
        self.commit()

    @sqlalchemy_additional_actions()
    def filter_by(self, model, query: Optional[Query] = None, **kwargs):
        if query:
            return query.filter_by(**kwargs)
        return model.query.filter_by(**kwargs)

    @sqlalchemy_additional_actions()
    def filter(self, model, query: Optional[Query] = None, *args, **kwargs):
        if query:
            return query.filter(*args, **kwargs)
        return model.query.filter(*args, **kwargs)

    def commit(self, **kwargs):
        return self.db.session.commit(**kwargs)

    def add(self, *args, **kwargs):
        return self.db.session.add(*args)

    def delete(self, item_id: str, model, **kwargs):
        model.query.filter_by(id=item_id).delete()
        self.commit()

    def get_all(self, model, **kwargs):
        return model.query.all()

    def paginate(self, query: Query, page: int, per_page: int, **kwargs):
        return query.paginate(page, per_page, error_out=False)

    def count(self, query: Query, **kwargs):
        return query.count()

    def like(self, model, query: Query, field, pattern: str, **kwargs):
        model_field = getattr(model, field)
        return query.filter(model_field.like(pattern))

    def get_query(self, model, *args, **kwargs):
        return model.query


class BaseMainStorage:
    def __init__(self, db: BaseSQLAlchemyStorage, db_model, **kwargs):
        super().__init__(**kwargs)

        self.db = db
        self.model = db_model

    @_trace()
    def get(self, item_id: str):
        return self.db.get(item_id=item_id, model=self.model)

    @_trace()
    def delete(self, item_id: str):
        return self.db.delete(item_id=item_id, model=self.model)

    @_trace()
    def filter_by(self, _first=None, _sort_by=None, **kwargs):
        return self.db.filter_by(model=self.model, _first=_first, **kwargs)

    @_trace()
    def filter(self, _first=None, _sort_by=None, *args, **kwargs):
        return self.db.filter(model=self.model, _first=_first, *args, **kwargs)

    @_trace()
    def create(self, **kwargs):
        return self.db.create(model=self.model, **kwargs)

    @_trace()
    def update(self, item_id: str, **kwargs):
        return self.db.update(item_id=item_id, model=self.model, **kwargs)

    @_trace()
    def get_all(self, **kwargs):
        return self.db.get_all(model=self.model, **kwargs)

    @_trace()
    def paginate(self, query, page: int, per_page: int, **kwargs):
        return self.db.paginate(query=query, page=page, per_page=per_page, **kwargs)

    @_trace()
    def count(self, query, **kwargs) -> int:
        return self.db.count(query, **kwargs)

    @_trace()
    def like(self, query, field, pattern: str, **kwargs):
        return self.db.like(
            query=query,
            model=self.model,
            field=field,
            pattern=pattern,
            **kwargs,
        )

    @_trace()
    def get_query(self, **kwargs):
        return self.db.get_query(model=self.model, **kwargs)
