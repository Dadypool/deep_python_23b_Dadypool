"Homework 2 with a parser func"


from typing import Callable
import json


def parse_json(
    json_str: str,
    keyword_callback: Callable[[str], any],
    required_fields: list[str] = None,
    keywords: list[str] = None,
) -> None:
    "Parses keywords from required fields"

    if not isinstance(json_str, str):
        raise TypeError("json_str must be a string")

    if not isinstance(required_fields, list) or not isinstance(keywords, list):
        raise TypeError("required_fields and keywords must be lists")

    for field in required_fields:
        if not isinstance(field, str):
            raise TypeError("required_fields must be list containing strings")

    for keyword in keywords:
        if not isinstance(keyword, str):
            raise TypeError("keywords must be list containing strings")

    json_doc = json.loads(json_str)

    for keyword in keywords:
        for field in required_fields:
            if field in json_doc:
                for field_keyword in json_doc[field].split():
                    if keyword.casefold() in field_keyword.casefold():
                        keyword_callback(keyword)
