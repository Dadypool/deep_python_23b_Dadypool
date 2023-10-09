"Homework 1 with tests for file_filter.py"

import unittest
from unittest.mock import patch, mock_open
from io import StringIO

from file_filter import filter_file


class TestFileFilter(unittest.TestCase):
    "Class with tests"

    def setUp(self):
        self.emmul_file = StringIO(
            "brave NeW\nBraveNEW\nHeLlO\nWorld extra info\nBraveNEW"
        )

    def test_incorrect_fileobj(self):
        "Tests if file_obj neither file object nor filename"

        with self.assertRaises(TypeError) as err:
            next(filter_file(0, []))

        self.assertEqual(TypeError, type(err.exception))
        self.assertEqual(
            "file_obj must be a file object or a file name", str(err.exception)
        )

    @patch("builtins.open", new_callable=mock_open, read_data="Hello\nbrave NeW\nWORLD")
    def test_filename(self, mock_file):
        "Tests if give function a filename"

        excepted_answer = ["brave NeW\n", "WORLD"]
        answer = []
        for line in filter_file("data.txt", ["world", "neW"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)

        mock_file.assert_called_once_with("data.txt", "r", encoding="UTF-8")

    def test_file_object(self):
        "Tests if give function a file object"

        excepted_answer = ["brave NeW\n", "World extra info\n"]
        answer = []

        for line in filter_file(self.emmul_file, ["world", "neW"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)

    def test_several_keywords_in_one_line(self):
        "Tests several keywords match in one line"

        excepted_answer = ["brave NeW\n"]
        answer = []
        for line in filter_file(self.emmul_file, ["BRAVE", "new"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)

    def test_nothing_found(self):
        "Test any keyword doesnt match"

        answer = []
        for line in filter_file(self.emmul_file, ["Some", "thing"]):
            answer.append(line)
        self.assertEqual(answer, [])

    def test_keywords_case(self):
        "Test keywords are case independent"

        excepted_answer = ["brave NeW\n", "HeLlO\n"]
        answer = []
        for line in filter_file(self.emmul_file, ["BRAVE", "hello"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)

    def test_keyword_matc_whole_line(self):
        "Test keyword match the whole line"

        excepted_answer = ["HeLlO\n"]
        answer = []
        for line in filter_file(self.emmul_file, ["HeLlO"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)

    def test_one_keyword_in_several_lines(self):
        "Test one keyword match in several lines"

        excepted_answer = ["BraveNEW\n", "BraveNEW"]
        answer = []
        for line in filter_file(self.emmul_file, ["BraveNEW"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)
