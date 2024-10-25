# pylint: disable=W1514,R0904

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

    def test_empty_stop_words(self):
        """
        Проверка, что если список стоп-слов пустой,
        строки возвращаются без фильтрации
        """
        search_words = ["роза"]
        stop_words = []

        expected_output = [
            "а Роза упала на лапу Азора",
            "И ещё одна строка с Роза",
        ]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_search_word_is_substring(self):
        """
        Проверка, что строка не возвращается, если слово для поиска является
        подсловом другого слова
        """
        search_words = ["роз", "стоп-слов"]
        stop_words = []

        expected_output = ["И последняя строка без стоп-слов"]

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

    def test_file_not_found(self):
        """
        Проверка, что при попытке открыть несуществующий файл
        возникает исключение
        """
        search_words = ["роза"]
        stop_words = ["азора"]

        with self.assertRaises(FileNotFoundError):
            with open("non_existent_file.txt", "r") as file:
                next(line_filter(file, search_words, stop_words))

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

    def test_case_insensitive_search(self):
        """
        Проверка фильтрации без учета регистра
        """
        search_words = ["РоЗа"]
        stop_words = ["АзОра"]

        expected_output = ["И ещё одна строка с Роза"]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_multiple_search_words_in_line(self):
        """
        Проверка фильтрации, если строка содержит несколько искомых слов
        """
        search_words = ["роза", "тестовая", "одна", "упала"]
        stop_words = []

        expected_output = [
            "а Роза упала на лапу Азора",
            "Это просто тестовая строка",
            "И ещё одна строка с Роза",
        ]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_matches_whole_search_word_tokenization(self):
        """
        Проверка, что строка возвращается, если поиск совпадает с целой строкой
        (предобработка токенизация)
        """
        search_words = "a Роза упала на лапу Азора".split()  # токенизация слов
        stop_words = []

        expected_output = [
            "а Роза упала на лапу Азора",
            "И ещё одна строка с Роза",
            "Строка с стоп-словом Азора",
        ]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_matches_whole_search_word_no_tokenization(self):
        """
        Проверка, что строка возвращается, если поиск совпадает с целой строкой
        (без предобработки)
        """
        search_words = ["a Роза упала на лапу Азора"]  # без токенизации
        stop_words = []

        expected_output = []

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_multiple_search_words_and_stop_words_in_line(self):
        """
        Проверка фильтрации, если строка содержит
        несколько искомых слов и стоп-слов
        """
        search_words = ["роза", "тестовая", "стоп-слов"]
        stop_words = ["строка", "одна"]
        expected_output = [
            "а Роза упала на лапу Азора",
        ]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_matches_whole_stop_words_tokenization(self):
        """
        Проверка, что строка возвращается, если поиск стоп-слов совпадает
        с целой строкой (предобработка токенизация)
        """
        search_words = ["роза", "стоп-слов"]
        stop_words = "a Роза упала на лапу Азора".split()  # токенизация слов

        expected_output = ["И последняя строка без стоп-слов"]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_line_matches_whole_stop_words_no_tokenization(self):
        """
        Проверка, что строка возвращается, если поиск стоп-слов совпадает
        с целой строкой (без предобработки)
        """
        search_words = ["роза"]
        stop_words = ["a Роза упала на лапу Азора"]  # без токенизации

        expected_output = [
            "а Роза упала на лапу Азора",
            "И ещё одна строка с Роза",
        ]

        result = list(line_filter(self.text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_single_word_per_line_with_search(self):
        """
        Проверка, что строки возвращаются, если они содержат только одно слово,
        которое присутствует в списке search_words
        """
        single_word_text = """роза\nазора\nтестовая\nстрока\nслово"""
        binary_stream = BytesIO()

        text_wrapper = TextIOWrapper(binary_stream, encoding="utf-8")
        text_wrapper.write(single_word_text)
        text_wrapper.flush()

        binary_stream.seek(0)

        search_words = ["роза", "строка"]
        stop_words = []

        expected_output = ["роза", "строка"]

        result = list(line_filter(text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_single_word_per_line_with_stop_words(self):
        """
        Проверка, что строки исключаются, если они содержат только одно слово,
        которое присутствует в списке stop_words
        """
        single_word_text = """роза\nазора\nтестовая\nстрока\nслово"""
        binary_stream = BytesIO()

        text_wrapper = TextIOWrapper(binary_stream, encoding="utf-8")
        text_wrapper.write(single_word_text)
        text_wrapper.flush()

        binary_stream.seek(0)

        search_words = ["роза", "строка", "слово"]
        stop_words = ["азора", "строка"]

        expected_output = ["роза", "слово"]

        result = list(line_filter(text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_repeating_search_words_in_line(self):
        """
        Проверка, что строка возвращается,
        если одно из искомых слов повторяется несколько раз
        """
        repeating_word_text = (
            """роза роза роза\nазора азора\nтест тест тест\nслово слово слово"""
        )

        binary_stream = BytesIO()

        text_wrapper = TextIOWrapper(binary_stream, encoding="utf-8")
        text_wrapper.write(repeating_word_text)
        text_wrapper.flush()

        binary_stream.seek(0)

        search_words = ["роза", "тест"]
        stop_words = []
        expected_output = ["роза роза роза", "тест тест тест"]
        result = list(line_filter(text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)

    def test_repeating_words_with_stop_words(self):
        """
        Проверка, что строка не возвращается,
        если она содержит повторяющееся искомое слово и стоп-слово
        """
        repeating_word_text = (
            """роза роза роза\nазора азора\nтест тест тест\nслово слово слово"""
        )

        binary_stream = BytesIO()

        text_wrapper = TextIOWrapper(binary_stream, encoding="utf-8")
        text_wrapper.write(repeating_word_text)
        text_wrapper.flush()

        binary_stream.seek(0)

        search_words = ["роза", "тест"]
        stop_words = ["азора", "роза"]

        expected_output = ["тест тест тест"]

        result = list(line_filter(text_wrapper, search_words, stop_words))
        self.assertEqual(result, expected_output)
