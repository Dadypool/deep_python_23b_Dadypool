#! /usr/bin/env python3

import json
import unittest

import ujson

import cjson


class TestCjson(unittest.TestCase):
    def test_loads(self):
        json_str = '{"hello": "world", "num": 10, "key": "value"}'

        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(json_doc, cjson_doc)

    def test_dumps(self):
        json_str = '{"hello": "world", "num": 10, "key": "value"}'

        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)

        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(json_doc, cjson_doc)
