import re
from typing import Any, Union
from dotwiz import DotWiz


class MatchingError(Exception):
    pass


async def key_fetcher(body: dict, pattern_item: str) -> Any:
    re_result = re.findall('^key:(.*)', pattern_item)
    if not re_result:
        raise MatchingError
    key = re_result[0]
    return body[key]


async def index_fetcher(body: Union[tuple, dict, list], pattern_item: str) -> Any:
    re_result = re.findall('^index:(.*)', pattern_item)
    if not re_result:
        raise MatchingError
    index = int(re_result[0])
    return body[index]


async def model_fetcher(body: dict, pattern_item: str) -> Any:
    re_result = re.findall('^model:(.*)', pattern_item)
    if not re_result:
        raise MatchingError
    if re_result[0] == 'dotwiz':
        return DotWiz(body)
    return body


fetch_functions = (key_fetcher, index_fetcher, model_fetcher)
