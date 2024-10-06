import unittest
from unittest.mock import Mock, call, patch
from typing import Type, Any, List

from retry_decorator import retry_deco

class TestRetryDecorator(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

    
    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_successful_execution(self):
        """Тест успешного выполнения без исключений"""
        mock_func = Mock(return_value=10)
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)
        result = decorated_func(2, 3)

        self.assertEqual(result, 10)
        mock_func.assert_called_once_with(2, 3)


    def test_retry_on_exception(self):
        """Тест на несколько попыток при возникновении исключения"""
        mock_func = Mock(side_effect=[ValueError("First failure"), 20])
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)
        result = decorated_func()

        self.assertEqual(result, 20)
        self.assertEqual(mock_func.call_count, 2)

    def test_max_retries_exceeded(self):
        """Тест на превышение максимального количества попыток"""
        mock_func = Mock(side_effect=ValueError("Always failing"))
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)

        with self.assertRaises(ValueError):
            decorated_func()

        self.assertEqual(mock_func.call_count, 3)

    def test_specific_exceptions_handled(self):
        """Тест обработки конкретных исключений"""
        mock_func = Mock(side_effect=ValueError("Expected failure"))
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3, exceptions=[ValueError])(mock_func)

        with self.assertRaises(ValueError):
            decorated_func()

        mock_func.assert_called_once()

    def test_invalid_retries_type(self):
        """Тест на неправильный тип параметра retries"""
        invalid_values = [
            12.34,
            {"key": "value"},
            {"set"},
            True,
            (1, 2, 3),
            ("value", "value"),
            object,
            [12, 23],
            [object],
            [None, 123],
        ]

        for invalid_value in invalid_values:
            with self.assertRaises(TypeError):
                retry_deco(retries=invalid_value)

    def test_invalid_exceptions_type(self):
        """Тест на неправильный тип параметра exceptions"""
        invalid_values = [
            123,
            12.34,
            {"key": "value"},
            {"set"},
            True,
            (1, 2, 3),
            ("value", "value"),
            object,
            [12, 23],
            [None, 123],
        ]

        for invalid_value in invalid_values:
            with self.assertRaises(TypeError):
                retry_deco(exceptions=invalid_value)

    def test_retry_on_general_exception(self):
        """Тест на повторение функции при любом исключении"""
        mock_func = Mock(side_effect=Exception("General exception"))
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)

        with self.assertRaises(Exception):
            decorated_func()

        self.assertEqual(mock_func.call_count, 3)

    def test_no_exceptions_raised(self):
        """Тест для функции, которая не вызывает исключений"""
        mock_func = Mock(return_value=8)
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)
        result = decorated_func(2, 4)

        self.assertEqual(result, 8)
        mock_func.assert_called_once_with(2, 4)

    def test_retry_deco_with_None(self):
        """Тест на работу декоратора с None в параметрах retries и exceptions"""
        mock_func = Mock(return_value=5)
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=None, exceptions=None)(mock_func)
        result = decorated_func(2, 3)

        self.assertEqual(result, 5)
        mock_func.assert_called_once_with(2, 3)

    def test_retry_on_multiple_exceptions(self):
        """Тест на работу с несколькими видами исключений"""
        mock_func = Mock(side_effect=[TypeError("First failure"), ValueError("Second failure"), "Success"])
        mock_func.__name__ = "mock_func"

        decorated_func = retry_deco(retries=3)(mock_func)
        result = decorated_func()

        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 3)

    def test_zero_retries(self):
        """Тест на случай, если количество попыток ноль или отрицательное число"""
        mock_func = Mock()
        mock_func.__name__ = "mock_func"

        with self.assertRaises(ValueError):
            retry_deco(retries=0)(mock_func)

        mock_func.assert_not_called()
        
        with self.assertRaises(ValueError):
            retry_deco(retries=-5)(mock_func)

        mock_func.assert_not_called()
