import re
from typing import Any


class MatchingError(Exception):
    pass


async def key_fetcher(body: dict, pattern_item: str) -> Any:
    re_result = re.findall('key:(.*?)', pattern_item)
    if not re_result:
        raise MatchingError
    key = re_result[0]
    return body[key]


async def index_fetcher(body: dict, pattern_item: str) -> Any:
    re_result = re.findall('index:(.*?)', pattern_item)
    if not re_result:
        raise MatchingError
    index = int(re_result[0])
    return body[index]


fetch_functions = (key_fetcher, index_fetcher)
