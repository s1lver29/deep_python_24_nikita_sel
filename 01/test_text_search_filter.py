import unittest
from io import TextIOWrapper, BytesIO

from .text_search_filter import line_filter


class TestLineFilter(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

        self.text = """а Роза упала на лапу Азора
Это просто тестовая строка
Без слов поиска
И ещё одна строка с Роза
Строка с стоп-словом Азора
И последняя строка без стоп-слов"""
        binary_stream = BytesIO()
        self.text_wrapper = TextIOWrapper(binary_stream, encoding="utf-8")

        self.text_wrapper.write(self.text)
        self.text_wrapper.flush()
        binary_stream.seek(0)

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_line_filter_with_search_words(self):
        """
        Проверка фильтрации строк с совпадениями по искомым словам
        """
        search_words = ["роза"]
        stop_words = ["азора"]

        expected_output = ["И ещё одна строка с Роза"]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_filter_with_no_matches(self):
        """
        Проверка, что нет строк, соответствующих искомым словам
        """
        search_words = ["слово"]
        stop_words = ["азора"]

        expected_output = []

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_filter_with_only_stop_words(self):
        """
        Проверка, что строки, которые определены там и там не возвращаются
        """
        search_words = ["роза"]
        stop_words = ["роза"]

        expected_output = []

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_filter_empty_file(self):
        """
        Проверка работы фильтра на пустом файле
        """
        binary_stream = BytesIO()
        empty_file = TextIOWrapper(binary_stream, encoding="utf-8")

        search_words = ["роза"]
        stop_words = ["азора"]

        expected_output = []

        result = list(line_filter(empty_file, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_invalid_file_type(self):
        """
        Проверка, что передача неверного типа файла вызывает TypeError
        """
        search_words = ["роза"]
        stop_words = ["азора"]

        with self.assertRaises(TypeError):
            next(line_filter(123, search_words, stop_words))

    def test_invalid_search_words_type(self):
        """
        Проверка, что передача некорректного типа для
        искомых слов вызывает TypeError
        """
        stop_words = ["азора"]

        with self.assertRaises(TypeError):
            next(line_filter(self.text_wrapper, "не список", stop_words))

    def test_invalid_stop_words_type(self):
        """
        Проверка, что передача некорректного типа для
        стоп-слов вызывает TypeError
        """
        search_words = ["роза"]

        with self.assertRaises(TypeError):
            next(line_filter(self.text_wrapper, search_words, "не список"))
