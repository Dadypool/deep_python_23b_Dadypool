"Homework 2 with tests for parser function"

import unittest
from unittest.mock import Mock, patch, call

from parse import parse_json


class TestParse(unittest.TestCase):
    "Class with tests"

    def setUp(self):
        self.mock_callback_func = Mock()
        self.json_str = '{"key1": "Word1 word2 word3 word3", "key2": "word2 word3"}'

    def test_no_json(self):
        "Tests if json_str parameter is not str"

        with self.assertRaises(TypeError):
            parse_json(None, self.mock_callback_func)

    def test_json_loads(self):
        "Test json.loads function to be called once with json_str argument"

        with patch("json.loads", return_value={"key1": "word2"}) as mock_load:
            parse_json("mock.json", self.mock_callback_func, ["key1"], ["word2"])
            mock_load.assert_called_once_with("mock.json")
        self.mock_callback_func.assert_called_once_with("word2")

    def test_callback_once(self):
        "Tests callback function to be called one time"

        self.assertEqual(
            None,
            parse_json(self.json_str, self.mock_callback_func, ["key1"], ["word2"]),
        )
        self.mock_callback_func.assert_called_once_with("word2")

    def test_callback_not_called(self):
        "Tests callback function to be not called"

        parse_json(self.json_str, self.mock_callback_func, ["key2"], ["word5"])
        self.mock_callback_func.assert_not_called()

    def test_callback_one_keyword_in_several_fields(self):
        "Tests callback function to be called several times with one keyword in diff fields"

        parse_json(self.json_str, self.mock_callback_func, ["key1", "key2"], ["word2"])
        self.mock_callback_func.assert_called_with("word2")
        self.assertEqual(2, self.mock_callback_func.call_count)

    def test_one_keyword_in_one_field_several_times(self):
        "Tests callback function to be called several times with one keyword in one field"

        parse_json(self.json_str, self.mock_callback_func, ["key1"], ["word3"])
        self.mock_callback_func.assert_called_with("word3")
        self.assertEqual(2, self.mock_callback_func.call_count)

    def test_callback_several_keywords_in_one_field(self):
        "Tests callback function to be called several times with different keywords"

        parse_json(self.json_str, self.mock_callback_func, ["key1"], ["Word1", "word2"])
        self.assertEqual(
            [call("Word1"), call("word2")], self.mock_callback_func.mock_calls
        )

    def test_no_fields_no_keywords(self):
        "Tests parse function without fields and keywrods arguments"

        with self.assertRaises(TypeError):
            parse_json(self.json_str, self.mock_callback_func)
            self.mock_callback_func.assert_not_called()

    def test_fields_keywords_with_diff_types(self):
        "Tests parse function with fields and keywrods as lists with different types"

        with self.assertRaises(TypeError):
            parse_json(self.json_str, self.mock_callback_func, ["key1", 3], ["word1"])
            self.mock_callback_func.assert_not_called()

        with self.assertRaises(TypeError):
            parse_json(self.json_str, self.mock_callback_func, ["key1"], ["Word1", 2])
            self.mock_callback_func.assert_not_called()

    def test_keyfields_case(self):
        "Tests fields must be case dependent"

        parse_json(self.json_str, self.mock_callback_func, ["Key1"], ["word2"])
        self.mock_callback_func.assert_not_called()

    def test_keywords_case(self):
        "Tests keywords must be case independent"

        parse_json(self.json_str, self.mock_callback_func, ["key1"], ["word1", "WORD2"])
        self.assertEqual(
            [call("word1"), call("WORD2")], self.mock_callback_func.mock_calls
        )
