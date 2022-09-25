import contextlib
import json
import re
from typing import Any, Tuple

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
    return body


async def replace_in_json(item: dict, pattern: str, replace_from: dict) -> dict:
    string_like_json = json.dumps(item)
    for matched_item in set(re.findall(pattern, string_like_json)):
        replace_from_key, other_string = await split_first(matched_item, ".")
        replace_to = replace_from.get(replace_from_key)
        
        if replace_to is None:
            continue

        replace_to = await recusivly_resolve_string(object=replace_to, string=other_string)

        string_like_json = string_like_json.replace(matched_item, replace_to)

    return json.loads(string_like_json)


async def split_first(string: str, delimiter: str) -> Tuple[str, str]:
    try:
        index_of_dot = string.index(delimiter)
        return string[:index_of_dot], string[index_of_dot + 1:]
    except ValueError:
        return string, ''


async def recusivly_resolve_string(object: Any, string: str) -> Any:
    """
    :param object: any object
    :param string: pattern, that starts with name of attribute and
                   possibly continue with other attributes with delimiter of dot "."
                   attributes can also have fetching index or key

    if
    object={'a':[{'b':1}] (Lets pretend that different dicts is instances of a some different classes)
    string='a[0].b'
    then return will be 1

    with string='a'
    return will be [{'b': 1}]



    remark:
    if your key of a dict should have str type, then close it with double quotes
    :return:
    """
    if not string:
        return object

    resolved_attribute, string = split_first(string=string, delimiter='.')

    try:
        index_of_bracket = resolved_attribute.index('[')
    except ValueError:
        index_of_bracket = 0
    if index_of_bracket:
        resolved_attribute, key = resolved_attribute[:index_of_bracket], \
                                  resolved_attribute[index_of_bracket + 1: -1]

        key = key[1:-1] if '"' in key else int(key)

        return await recusivly_resolve_string(object=getattr(object, resolved_attribute)[key],
                                              string=string)

    return await recusivly_resolve_string(object=getattr(object, resolved_attribute),
                                          string=string)
