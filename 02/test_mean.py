"Homework 2 with tests for mean decorator"

import unittest
from unittest.mock import Mock, patch
from io import StringIO

from mean import mean


class TestDecor(unittest.TestCase):
    "Class with tests"

    def setUp(self):
        self.mock_func = Mock()
        self.mock_func.return_value = 99

    def test_base_work(self):
        "Tests base work of the decorator. Number of func calss equal to k"

        param_k = 10
        dec = mean(param_k)(self.mock_func)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            for i in range(1, param_k + 1):
                self.assertEqual(dec(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= param_k else param_k} calls", mock_out.getvalue()
                )
        self.assertEqual(param_k, self.mock_func.call_count)

    def test_calls_less_k(self):
        "Tests func calls would be less than k"

        n_calls = 5
        param_k = 8
        dec = mean(param_k)(self.mock_func)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            for i in range(1, n_calls + 1):
                self.assertEqual(dec(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= param_k else param_k} calls", mock_out.getvalue()
                )
        self.assertEqual(n_calls, self.mock_func.call_count)

    def test_calls_more_k(self):
        "Tests func calls would be less than k"

        n_calls = 20
        param_k = 8
        dec = mean(param_k)(self.mock_func)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            for i in range(1, n_calls + 1):
                self.assertEqual(dec(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= param_k else param_k} calls", mock_out.getvalue()
                )
        self.assertEqual(n_calls, self.mock_func.call_count)

    def test_mean_without_k(self):
        "Tests mean decor without param k. k must be 10 by default"

        default = 10
        n_calls = 15
        dec = mean()(self.mock_func)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            for i in range(1, n_calls + 1):
                self.assertEqual(dec(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= default else default} calls", mock_out.getvalue()
                )
        self.assertEqual(n_calls, self.mock_func.call_count)

    def test_two_decor_at_one_time(self):
        "Test two decorators at one time. They must contain different call queues"

        n_calls = 30
        param_k1 = 5
        param_k2 = 10
        dec1 = mean(param_k1)(self.mock_func)
        dec2 = mean(param_k2)(self.mock_func)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            for i in range(1, n_calls + 1):
                self.assertEqual(dec1(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= param_k1 else param_k1} calls",
                    mock_out.getvalue(),
                )
                self.assertEqual(dec2(), self.mock_func.return_value)
                self.assertIn(
                    f"last {i if i <= param_k2 else param_k2} calls",
                    mock_out.getvalue(),
                )
        self.assertEqual(n_calls * 2, self.mock_func.call_count)

    def test_decor_called_once(self):
        "Tests that decor func called only once"

        with patch("mean.mean") as mock_mean:
            dec = mock_mean(10)(self.mock_func)
            for _ in range(10):
                dec()
            mock_mean.assert_called_once()
