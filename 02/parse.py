"Homework 2 with a parser func"

import json


def parse_json(
    json_str: str, required_fields=None, keywords=None, keyword_callback=any
):
    "Parses keywords from required fields"

    json_doc = json.loads(json_str)

    for field in required_fields:
        for keyword in keywords:
            if keyword.casefold() in json_doc[field].casefold():
                keyword_callback(keyword)
