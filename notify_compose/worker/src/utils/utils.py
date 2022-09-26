import contextlib
import json
import re
from typing import Any, Tuple, Optional

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
                body = await func(body=body, pattern_item=item)
            break
    return body


async def replace_in_json(item: dict, pattern: str, replace_from: dict, pattern_enclosing: str) -> dict:
    string_like_json = json.dumps(item)
    for matched_item in set(re.findall(pattern, string_like_json)):
        replace_from_key, other_string = await split_first(matched_item, ".")
        replace_to = replace_from.get(replace_from_key)

        if replace_to is None:
            continue

        replace_to = await recursivly_resolve_string(object_=replace_to, string=other_string)

        string_like_json = string_like_json.replace(pattern_enclosing % matched_item, replace_to)

    return json.loads(string_like_json)


async def index(string: str, sub_string: str, default_: Optional[Any] = -1):
    try:
        return string.index(sub_string)
    except ValueError:
        return default_


async def split_first(string: str, delimiter: str) -> Tuple[str, str]:
    try:
        index_of_dot = string.index(delimiter)
        return string[:index_of_dot], string[index_of_dot + 1:]
    except ValueError:
        return string, ''


async def recursivly_key_getter(object_: Any, string: str) -> Any:
    """

    :param object_: any object that supports access by index/key
    :param string: string of square brackets with keys in it for ex. : [1]["key"][2]
    not [[1]], only sequence of [] with keys in it

    remark:
    if your key of a dict should have str type, then close it with double quotes
    :return:
    """
    if not string:
        return object_
    index_of_closed = await index(string=string, sub_string=']')
    key, string = string[1:index_of_closed], string[index_of_closed + 1:]
    key = key[1:-1] if '"' in key else int(key)
    return await recursivly_key_getter(object_=object_[key], string=string)


async def recursivly_resolve_string(object_: Any, string: str) -> Any:
    """
    :param object_: any object
    :param string: pattern, that starts with name of attribute and
                   possibly continue with other attributes with delimiter of dot "."
                   attributes can also have fetching index or key

    if
    object={'a':[{'b':1}] (Lets pretend that different dicts is instances of a some different classes)
    string='a[0].b'
    then return will be 1

    with string='a'
    return will be [{'b': 1}]

    :return:
    """
    if not string:
        return object_

    resolved_attribute, string = await split_first(string=string, delimiter='.')

    index_of_bracket = await index(string=resolved_attribute, sub_string='[')
    if index_of_bracket != -1:
        resolved_attribute, key_string = resolved_attribute[:index_of_bracket], \
                                         resolved_attribute[index_of_bracket:]
        object_ = getattr(object_, resolved_attribute) if resolved_attribute else object_

        object_ = await recursivly_key_getter(object_=object_, string=key_string)

        return await recursivly_resolve_string(object_=object_, string=string)

    return await recursivly_resolve_string(object_=getattr(object_, resolved_attribute),
                                           string=string)
