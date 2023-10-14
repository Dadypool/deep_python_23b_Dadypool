"Homework 1 with tests for predict.py"

from unittest import TestCase, mock

from predict import predict_message_mood


class TestPredict(TestCase):
    "Class with tests"

    def setUp(self):
        self.model = mock.Mock()
        self.model.predict.return_value = 0.5

    def test_base_work(self):
        "Test base work"

        self.assertEqual("норм", predict_message_mood("База", self.model))
        self.model.predict.assert_called_once_with("База")

        self.model.predict.return_value = 0.1
        self.assertEqual("неуд", predict_message_mood("Не норм", self.model))

        self.model.predict.return_value = 1.0
        self.assertEqual("отл", predict_message_mood("Пере норм", self.model))

    def test_edge_cases(self):
        "Tests edge cases"

        self.model.predict.return_value = 0.3
        self.assertEqual("норм", predict_message_mood("Около левый край", self.model))
        self.model.predict.assert_called_once_with("Около левый край")

        self.model.predict.return_value = 0.8
        self.assertEqual("норм", predict_message_mood("Около правый край", self.model))

        self.model.predict.return_value = 0.2
        self.assertEqual("неуд", predict_message_mood("Левый край", self.model))

        self.model.predict.return_value = 0.9
        self.assertEqual("отл", predict_message_mood("Правый край", self.model))

    def test_extra_edge_cases(self):
        "Tests edge cases that nearly close to threshholds"

        self.model.predict.return_value = 0.300000001
        self.assertEqual(
            "норм", predict_message_mood("Близко справа от левого края", self.model)
        )
        self.model.predict.assert_called_once_with("Близко справа от левого края")

        self.model.predict.return_value = 0.799999999
        self.assertEqual(
            "норм", predict_message_mood("Близко слева от правого края", self.model)
        )

        self.model.predict.return_value = 0.299999999
        self.assertEqual(
            "неуд", predict_message_mood("Близко слева от левого края", self.model)
        )

        self.model.predict.return_value = 0.900000001
        self.assertEqual(
            "отл", predict_message_mood("Близко справа от правого края", self.model)
        )

    def test_change_thresholds(self):
        "Test chainging tresholds"

        self.assertEqual("неуд", predict_message_mood("База", self.model, 0.6))
        self.model.predict.return_value = 0.9
        self.assertEqual("норм", predict_message_mood("Не норм", self.model, 0.3, 0.9))
        self.model.predict.return_value = 0.4
        self.assertEqual("отл", predict_message_mood("Пере норм", self.model, 0.1, 0.3))

    def test_model_called_once(self):
        "Test model predict func called once"

        predict_message_mood("База", self.model)
        self.model.predict.assert_called_once_with("База")
