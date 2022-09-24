import contextlib
import json
import re
from typing import Any

import orjson
from services.result_fetcher import MatchingError, fetch_functions


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes,
    # а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


async def fetch_result(body: dict, pattern: str) -> Any:
    for item in pattern.split(', '):
        for func in fetch_functions:
            with contextlib.suppress(MatchingError):
                body = func(body=body, pattern_item=item)
            break


async def replace_in_json(item: dict, pattern: str, replace_from: dict) -> dict:
    string_like_json = json.dumps(item)
    for matched_item in set(re.findall(pattern, string_like_json)):
        replace_to = replace_from.get(matched_item)
        if replace_to is None:
            continue
        string_like_json = string_like_json.replace(matched_item, replace_to)

    return json.loads(string_like_json)
