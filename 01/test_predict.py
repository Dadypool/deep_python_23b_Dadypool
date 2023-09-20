import unittest
from unittest import mock

from predict import SomeModel, predict_message_mood

class TestPredict(unittest.TestCase):
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR_DOWN")

    def test_init(self):
        print("INIT")

    def test_prediction(self):
        model = SomeModel()

        self.assertEqual("отл", predict_message_mood("Чапаев и пустота", model))
        self.assertEqual("неуд", predict_message_mood("Вулкан", model))