"Homework 1.3 tests for tasks 1 and 2"

import unittest
from unittest.mock import patch, mock_open

from file_filter import filter_file
from predict import SomeModel, predict_message_mood


class TestPredict(unittest.TestCase):
    "Class with tests"

    def setUp(self):
        self.model = SomeModel()

    def test_edge_cases(self):
        "Tests edge case"

        self.assertEqual("неуд", predict_message_mood("", self.model))

    def test_prediction(self):
        "Tests  predict_message_mood() function"

        self.assertEqual("неуд", predict_message_mood("Чиуауа", self.model))
        self.assertEqual("норм", predict_message_mood("Чапаев и пустота", self.model))
        self.assertEqual("отл", predict_message_mood("Встреск", self.model))


class TestFileFilter(unittest.TestCase):
    "Class with tests"

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

    def read(self):
        "Immitates readlines() method of TextIOBase class"

        lines = ["Hello\n", "brave NeW\n", "WORLD", "sd", "dsfsdf", "ds"]
        for line in lines:
            yield line

    @patch("io.TextIOBase", spec=True)
    def test_file_object(self, mock_file):
        "Tests if give function a file object"

        mock_file.__iter__.side_effect = self.read

        excepted_answer = ["brave NeW\n", "WORLD"]
        answer = []

        for line in filter_file(mock_file, ["world", "neW"]):
            answer.append(line)
        self.assertEqual(answer, excepted_answer)
