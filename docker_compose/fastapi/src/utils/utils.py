from typing import TypeVar, Sequence

import orjson
from fastapi_pagination import Params, Page
from pydantic import conint

T = TypeVar("T")


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes,
    # а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


def paginate(
        items: Sequence[T], total: conint(ge=1), page: conint(ge=1),
        size: conint(ge=1)
) -> Page[T]:
    params = Params(page=page, size=size)
    return Page.create(items=items, total=total, params=params)