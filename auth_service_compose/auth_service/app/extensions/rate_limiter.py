from http import HTTPStatus

from flask import request

from core.settings import settings
from db.cache_db import get_cache_db
from schemas.base.responses import TOO_MANY_REQUESTS
from utils.utils import make_error_response


def rate_limit():
    cache_db = get_cache_db()
    pipe = cache_db.pipeline()

    key = request.remote_addr

    pipe.incr(key, 1)
    pipe.expire(key, 59)

    result = pipe.execute()
    request_number = result[0]
    if request_number > settings.REQUEST_LIMIT_PER_MINUTE:
        return make_error_response(msg=TOO_MANY_REQUESTS,
                                   status=HTTPStatus.TOO_MANY_REQUESTS)