# pylint: disable=I1101

import unittest

import custom_json


class TestCustomJson(unittest.TestCase):
    def test_loads_valid(self):
        """Тест корректного разбора JSON-строк."""
        self.assertEqual(
            custom_json.loads('{"hello": 10, "world": "value"}'),
            {"hello": 10, "world": "value"},
        )
        self.assertEqual(
            custom_json.loads('{"number": 123, "text": "example"}'),
            {"number": 123, "text": "example"},
        )
        self.assertEqual(
            custom_json.loads('{"number": -230, "text": "-example"}'),
            {"number": -230, "text": "-example"},
        )
        self.assertEqual(
            custom_json.loads('{"number": 0, "text": ""}'),
            {"number": 0, "text": ""},
        )

    def test_loads_invalid(self):
        """Тест обработки некорректных JSON-строк."""
        with self.assertRaises(TypeError):
            custom_json.loads(
                '{"hello": 10, "world": value}'
            )  # Значение без кавычек
        with self.assertRaises(TypeError):
            custom_json.loads(
                '{hello: 10, "world": "value"}'
            )  # Ключ без кавычек
        with self.assertRaises(TypeError):
            custom_json.loads('["not", "an", "object"]')  # Не объект
        with self.assertRaises(TypeError):
            custom_json.loads("")  # Пустая строка

    def test_dumps_valid(self):
        """Тест корректной сериализации словарей."""
        self.assertEqual(
            custom_json.dumps({"hello": 10, "world": "value"}),
            '{"hello": 10, "world": "value"}',
        )
        self.assertEqual(
            custom_json.dumps({"number": 123, "text": "example"}),
            '{"number": 123, "text": "example"}',
        )
        self.assertEqual(
            custom_json.dumps({"number": -230, "text": "-example"}),
            '{"number": -230, "text": "-example"}',
        )
        self.assertEqual(
            custom_json.dumps({"number": 0, "text": ""}),
            '{"number": 0, "text": ""}',
        )

    def test_dumps_invalid(self):
        """Тест обработки некорректных данных для сериализации."""
        with self.assertRaises(TypeError):
            custom_json.dumps(
                ["not", "a", "dict"]
            )  # Передан список вместо словаря
        with self.assertRaises(TypeError):
            custom_json.dumps(
                {"key": {"nested": "object"}}
            )  # Вложенные объекты
        with self.assertRaises(TypeError):
            custom_json.dumps({"key": None})  # None не поддерживается

    def test_round_trip(self):
        """Тест преобразования туда и обратно."""
        json_str = '{"hello": 10, "world": "value"}'
        parsed = custom_json.loads(json_str)
        serialized = custom_json.dumps(parsed)
        self.assertEqual(serialized, json_str)


class TestCustomJsonEdgeCases(unittest.TestCase):
    def test_loads_empty_object(self):
        """Тест парсинга пустого JSON-объекта."""
        self.assertEqual(custom_json.loads("{}"), {})

    def test_loads_large_object(self):
        """Тест парсинга большого JSON-объекта."""
        json_str = (
            "{" + ", ".join([f'"key{i}": {i}' for i in range(1000)]) + "}"
        )
        expected_dict = {f"key{i}": i for i in range(1000)}
        self.assertEqual(custom_json.loads(json_str), expected_dict)

    def test_loads_edge_numbers(self):
        """Тест пограничных значений чисел."""
        json_str = '{"min": -2147483646, "max": 2147483646}'
        expected_dict = {"min": -2147483646, "max": 2147483646}
        self.assertEqual(custom_json.loads(json_str), expected_dict)

    def test_dumps_empty_object(self):
        """Тест сериализации пустого словаря."""
        self.assertEqual(custom_json.dumps({}), "{}")

    def test_dumps_large_object(self):
        """Тест сериализации большого словаря."""
        large_dict = {f"key{i}": i for i in range(1000)}
        expected_json = (
            "{" + ", ".join([f'"key{i}": {i}' for i in range(1000)]) + "}"
        )
        self.assertEqual(custom_json.dumps(large_dict), expected_json)

    def test_round_trip_empty_object(self):
        """Тест преобразования пустого объекта туда и обратно."""
        json_str = "{}"
        parsed = custom_json.loads(json_str)
        serialized = custom_json.dumps(parsed)
        self.assertEqual(serialized, json_str)

    def test_round_trip_large_object(self):
        """Тест преобразования большого объекта туда и обратно."""
        json_str = (
            "{" + ", ".join([f'"key{i}": {i}' for i in range(1000)]) + "}"
        )
        parsed = custom_json.loads(json_str)
        serialized = custom_json.dumps(parsed)
        self.assertEqual(serialized, json_str)
