import asyncio
import contextlib
from functools import wraps
from typing import TypeVar, Sequence

import jwt
import orjson
from aiohttp import ClientConnectorError
from fastapi import HTTPException
from fastapi_pagination import Params, Page
from pydantic import conint

from core.config import settings

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


def decode_jwt(token: str):
    try:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=["HS256"])
    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(status_code=404, detail=str(e))


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            t = start_sleep_time
            while t < border_sleep_time:
                with contextlib.suppress(ClientConnectorError):
                    return await func(*args, **kwargs)
                t = t * factor
                t = t if t < border_sleep_time else border_sleep_time
                await asyncio.sleep(t)
            raise ConnectionError

        return inner

    return func_wrapper
