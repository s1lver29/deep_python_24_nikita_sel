# pylint: disable=R0904
import unittest
from .lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(2)
        print(f"\nStart test {self.id()}")

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_set_and_get(self):
        """Тест на добавление элемента и его последующее получение"""
        self.cache.set("k1", "val1")
        self.assertEqual(self.cache.get("k1"), "val1")

    def test_add_second_element(self):
        """Тест на добавление второго элемента в кэш и его доступность"""
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.assertEqual(self.cache.get("k2"), "val2")

    def test_get_nonexistent_key(self):
        """Тест, что при запросе несуществующего ключа возвращается None"""
        self.assertIsNone(self.cache.get("k3"))

    def test_eviction_of_lru_element(self):
        """
        Тест на вытеснение наименее недавно использованного элемента
        при достижении лимита
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")  # "k1" должен быть удалён, так как он LRU
        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_update_existing_key(self):
        """Тест на обновление значения для уже существующего ключа"""
        self.cache.set("k1", "val1")
        self.cache.set("k1", "new_val1")  # Обновляем значение для "k1"
        self.assertEqual(self.cache.get("k1"), "new_val1")

    def test_eviction_on_addition(self):
        """
        Тест вытеснение при добавлении нового элемента после
        достижения лимита
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")  # "k1" должен быть удалён, так как он LRU
        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_usage_with_subscript(self):
        """
        Тест на доступ к элементам кэша с помощью синтаксиса []
        для установки и получения значений
        """
        self.cache["k1"] = "val1"
        self.assertEqual(self.cache["k1"], "val1")

    def test_max_limit(self):
        """Тест, что при добавлении нового элемента после достижения лимита,
        наименее недавно использованный элемент вытесняется"""
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")  # "k1" должен быть удалён
        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_eviction_on_multiple_additions(self):
        """
        Тест на корректное вытеснение нескольких элементов
        при последовательных добавлениях
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")  # "k1" должен быть удалён
        self.cache.set("k4", "val4")  # "k2" должен быть удалён
        self.assertIsNone(self.cache.get("k2"))
        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertEqual(self.cache.get("k4"), "val4")

    def test_reaccessing_key_moves_it_to_front(self):
        """
        Тест, что доступ к существующему элементу обновляет его положение
        и предотвращает его вытеснение при добавлении новых элементов
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.get("k1")  # Должно переместить "k1" в начало
        self.cache.set(
            "k3", "val3"
        )  # "k2" должен быть удалён, так как он теперь LRU
        self.assertIsNone(self.cache.get("k2"))
        self.assertEqual(self.cache.get("k1"), "val1")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_zero_capacity(self):
        """
        Тест, что при создании кэша с нулевой ёмкостью выбрасывается ValueError
        """
        with self.assertRaises(ValueError) as context:
            LRUCache(0)
        self.assertEqual(
            str(context.exception),
            "Получено limit=0, <int>. limit должен быть > 0 и целочисленным",
        )

    def test_negative_capacity(self):
        """
        Тест, что при создании кэша с отрицательной ёмкостью
        выбрасывается ValueError
        """
        with self.assertRaises(ValueError) as context:
            LRUCache(-1)
        self.assertEqual(
            str(context.exception),
            "Получено limit=-1, <int>. limit должен быть > 0 и целочисленным",
        )

    def test_non_integer_capacity(self):
        """
        Тест, что при создании кэша с нецелочисленным значением
        выбрасывается ValueError
        """
        with self.assertRaises(ValueError) as context:
            LRUCache(3.5)
        self.assertEqual(
            str(context.exception),
            "Получено limit=3.5, <float>. "
            "limit должен быть > 0 и целочисленным",
        )

        with self.assertRaises(ValueError) as context:
            LRUCache("42")
        self.assertEqual(
            str(context.exception),
            "Получено limit='42', <str>. limit должен быть > 0 и целочисленным",
        )

        with self.assertRaises(ValueError) as context:
            LRUCache(None)
        self.assertEqual(
            str(context.exception),
            "Получено limit=None, <NoneType>. "
            "limit должен быть > 0 и целочисленным",
        )

    def test_cache_with_one_capacity(self):
        """
        Тест на кэш, который может хранить только один элемент
        """
        one_cache = LRUCache(1)
        one_cache.set("k1", "val1")
        self.assertEqual(one_cache.get("k1"), "val1")
        one_cache.set("k2", "val2")
        self.assertIsNone(one_cache.get("k1"))
        self.assertEqual(one_cache.get("k2"), "val2")

    def test_repeated_set_operations(self):
        """
        Тест на поведение при повторных добавлениях одного и того же ключа
        """
        self.cache.set("k1", "val1")
        self.cache.set("k1", "val1")
        self.cache.set("k1", "val1")
        self.assertEqual(self.cache.get("k1"), "val1")

    def test_all_elements_evicted(self):
        """
        Тест, что при добавлении большего количества элементов,
        чем ёмкость кэша, все старые элементы вытесняются
        """
        large_cache = LRUCache(3)
        large_cache.set("k1", "val1")
        large_cache.set("k2", "val2")
        large_cache.set("k3", "val3")
        large_cache.set("k4", "val4")
        large_cache.set("k5", "val5")
        large_cache.set("k6", "val6")
        self.assertIsNone(large_cache.get("k1"))
        self.assertIsNone(large_cache.get("k2"))
        self.assertIsNone(large_cache.get("k3"))
        self.assertEqual(large_cache.get("k4"), "val4")
        self.assertEqual(large_cache.get("k5"), "val5")
        self.assertEqual(large_cache.get("k6"), "val6")

    def test_access_pattern_affects_eviction(self):
        """
        Тест, что доступ к элементу обновляет его порядок
        и предотвращает его вытеснение
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")  # "k1" должен быть удалён
        self.cache.get("k2")  # Обращаемся к "k2" для обновления его позиции
        self.cache.set("k4", "val4")  # Теперь "k3" должен быть удалён
        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertIsNone(self.cache.get("k3"))
        self.assertEqual(self.cache.get("k4"), "val4")

    def test_clear_cache(self):
        """
        Тест, что при очистке кэша все элементы удаляются
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.cache.clear()  # Очищаем содержимое кэша
        self.assertIsNone(self.cache.get("k1"))
        self.assertIsNone(self.cache.get("k2"))

    def test_large_number_of_operations(self):
        """
        Тест на проверку стабильности кэша при большом количестве операций
        """
        large_cache = LRUCache(1000)
        for i in range(2000):
            large_cache.set(f"key{i}", f"value{i}")
        # Проверяем, что кэш содержит последние 1000 элементов
        for i in range(1000, 2000):
            self.assertEqual(large_cache.get(f"key{i}"), f"value{i}")
        # Проверяем, что первые 1000 элементов были вытеснены
        for i in range(1000):
            self.assertIsNone(large_cache.get(f"key{i}"))
