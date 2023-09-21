"Homework 1.1 tests"

import unittest

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
