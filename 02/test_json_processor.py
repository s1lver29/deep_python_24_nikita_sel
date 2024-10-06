# pylint: disable=R0801
import unittest
from unittest.mock import Mock

import json
from .json_processor import process_json


class TestProcessJson(unittest.TestCase):

    def setUp(self):
        print(f"\nStart test {self.id()}")

        self.invalid_values = [
            123,
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

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_invalid_json_str(self):
        """Невалидная строка JSON должна вызывать JSONDecodeError"""
        for invalid_value in self.invalid_values:
            with self.assertRaises(TypeError):
                process_json(invalid_value)

        with self.assertRaises(json.JSONDecodeError):
            process_json("")

        with self.assertRaises(json.JSONDecodeError):
            process_json('{"key": "value",}')

    def test_invalid_required_keys(self):
        """Невалидный список required_keys должен вызывать TypeError"""
        json_str = '{"key": "value"}'
        for invalid_value in self.invalid_values:
            with self.assertRaises(TypeError):
                process_json(json_str, required_keys=invalid_value)

    def test_invalid_tokens(self):
        """Невалидный список tokens должен вызывать TypeError"""
        json_str = '{"key": "value"}'
        for invalid_value in self.invalid_values:
            with self.assertRaises(TypeError):
                process_json(json_str, tokens=invalid_value)

    def test_invalid_callback(self):
        """Невалидный callback должен вызывать TypeError"""
        json_str = '{"key": "value"}'
        for invalid_value in self.invalid_values:
            with self.assertRaises(TypeError):
                process_json(json_str, callback=invalid_value)

    def test_callback_is_none(self):
        """Проверка поведения, если callback равен None"""
        json_str = '{"key1": "word1 word2", "key2": "word3 word4"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, callback=None)

        mock_callback.assert_not_called()

    def test_valid_case_no_tokens(self):
        """Валидация нормального случая без токенов"""
        mock_callback = Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        process_json(json_str, required_keys=["key1"], callback=mock_callback)

        mock_callback.assert_any_call("key1", "Word1")
        mock_callback.assert_any_call("key1", "word2")
        self.assertEqual(mock_callback.call_count, 2)

    def test_valid_case_with_tokens(self):
        """Базовый пример"""
        mock_callback = Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        process_json(
            json_str,
            required_keys=["key1"],
            tokens=["word1", "word2"],
            callback=mock_callback,
        )

        mock_callback.assert_any_call("key1", "word1")
        mock_callback.assert_any_call("key1", "word2")
        self.assertEqual(mock_callback.call_count, 2)

    def test_empty_json(self):
        """Пустой JSON"""
        mock_callback = Mock()
        process_json("{}", callback=mock_callback)

        mock_callback.assert_not_called()

    def test_no_required_keys_no_tokens(self):
        """required_keys и tokens не переданы, обрабатываются все ключи"""
        mock_callback = Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        process_json(json_str, callback=mock_callback)

        # Проверяем, что все ключи обрабатываются
        mock_callback.assert_any_call("key1", "Word1")
        mock_callback.assert_any_call("key1", "word2")
        mock_callback.assert_any_call("key2", "word3")
        mock_callback.assert_any_call("key2", "word4")
        self.assertEqual(mock_callback.call_count, 4)

    def test_no_required_keys(self):
        """required_keys не передан, обрабатываются все ключи"""
        mock_callback = Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        process_json(
            json_str,
            required_keys=None,
            tokens=["word1", "word4"],
            callback=mock_callback,
        )

        mock_callback.assert_any_call("key1", "word1")
        mock_callback.assert_any_call("key2", "word4")
        self.assertEqual(mock_callback.call_count, 2)

    def test_no_tokens(self):
        """tokens не переданы, обрабатываются слова без токенов"""
        mock_callback = Mock()
        json_str = '{"key1": "Word1 word2", "key2": "word3 word4"}'
        process_json(
            json_str,
            required_keys=["key1"],
            tokens=None,
            callback=mock_callback,
        )

        mock_callback.assert_any_call("key1", "Word1")
        mock_callback.assert_any_call("key1", "word2")
        self.assertEqual(mock_callback.call_count, 2)

    def test_token_processing_various_cases_no_required_keys(self):
        """
        Проверка обработки токенов с различными регистрами
        и повторениями
        """
        mock_callback = Mock()
        total_mock_calls = 0

        test_cases = [
            (
                # Повторение и регистры
                '{"key1": "word1 Word2 word1", "key2": "WORD2 wOrD4 word3"}',
                ["word1", "WORD2", "word4"],
                [
                    ("key1", "word1"),
                    ("key1", "WORD2"),
                    ("key1", "word1"),
                    ("key2", "WORD2"),
                    ("key2", "word4"),
                ],
            ),
            (
                # Повторения токенов
                '{"key1": "hello world hello", "key2": "HELLO world HelLO"}',
                ["hello", "WORLD"],
                [
                    ("key1", "hello"),
                    ("key1", "WORLD"),
                    ("key1", "hello"),
                    ("key2", "hello"),
                    ("key2", "WORLD"),
                    ("key2", "hello"),
                ],
            ),
            (
                # Повторение
                '{"key1": "Apple banana", "key2": "BaNaNa APPLE"}',
                ["banana"],
                [("key1", "banana"), ("key2", "banana")],
            ),
            (
                # Регистры
                '{"key1": "token1 TokEN2 token3", "key2": "ToKeN3 TOKEN1"}',
                ["token1", "token2", "TOKEN3"],
                [
                    ("key1", "token1"),
                    ("key1", "token2"),
                    ("key1", "TOKEN3"),
                    ("key2", "TOKEN3"),
                    ("key2", "token1"),
                ],
            ),
        ]

        for json_str, tokens, expected_calls in test_cases:
            process_json(json_str, tokens=tokens, callback=mock_callback)

            for key, token in expected_calls:
                mock_callback.assert_any_call(key, token)

            total_mock_calls += mock_callback.call_count
            mock_callback.reset_mock()

        total_expected_calls = sum(
            len(expected_calls) for _, _, expected_calls in test_cases
        )
        self.assertEqual(total_mock_calls, total_expected_calls)

    def test_no_partial_matches(self):
        """
        Проверка, что частичные совпадения токенов
        не вызывают callback
        """
        mock_callback = Mock()
        json_str = '{"key1": "word1 word1st", "key2": "word2 dsfword2"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_any_call("key1", "word1")
        mock_callback.assert_any_call("key2", "word2")
        self.assertEqual(mock_callback.call_count, 2)

    def test_tokens_as_substrings(self):
        """Проверка, что токены как подстроки не вызывают callback"""
        mock_callback = Mock()
        json_str = '{"key1": "word1 word2", "key2": "wordword4"}'
        required_keys = ["key1", "key2"]
        tokens = ["word", "word1", "word4"]

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_any_call("key1", "word1")
        self.assertEqual(mock_callback.call_count, 1)

    def test_case_sensitivity(self):
        """
        Проверка регистрозависимости ключей
        и регистронезависимости токенов
        """
        mock_callback = Mock()

        # Разный регистр в ключах и совпадающие токены
        json_str = '{"key1": "Word1 word2", "key2": "word2 word4"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["word1", "WORD2"]

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_any_call("key1", "word1")
        mock_callback.assert_any_call("key1", "WORD2")
        self.assertEqual(mock_callback.call_count, 2)

        # Токены различного регистра обрабатываются
        mock_callback.reset_mock()
        json_str = '{"key1": "word1 WORD1", "key2": "word2 word3"}'
        required_keys = ["key1"]
        tokens = ["WORD1", "word2"]

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_any_call("key1", "WORD1")
        mock_callback.assert_any_call("key1", "WORD1")
        self.assertEqual(mock_callback.call_count, 2)

        # # Отсутствие совпадений из-за различий в регистре ключей
        mock_callback.reset_mock()
        json_str = '{"key1": "word1 word2", "key2": "WORD3 WORD4"}'
        required_keys = ["keY1", "Key2"]
        tokens = ["word1", "word4"]

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_not_called()

        # # Повторяющиеся токены в поиске
        mock_callback.reset_mock()
        json_str = '{"key1": "word1 word2", "key2": "word2 word4"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "WORD1", "word2"]  # Повторяющийся токен

        process_json(json_str, required_keys, tokens, callback=mock_callback)

        mock_callback.assert_any_call("key1", "word1")
        mock_callback.assert_any_call("key1", "word2")
        mock_callback.assert_any_call("key2", "word2")
        self.assertEqual(mock_callback.call_count, 3)
