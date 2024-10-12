# pylint: disable=R0914,R0904
import unittest
from .custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_add_custom_lists_not_modified(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([4, 5, 6])
        cl1_copy = cl1[:]
        cl2_copy = cl2[:]
        cl1_id = id(cl1)
        cl2_id = id(cl2)

        cl3 = cl1
        cl3 = cl1 + cl2

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(cl2, cl2_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(cl2), cl2_id)

    def test_sub_custom_lists_not_modified(self):
        cl1 = CustomList([7, 8, 9])
        cl2 = CustomList([3, 2, 1])
        cl1_copy = cl1[:]
        cl2_copy = cl2[:]
        cl1_id = id(cl1)
        cl2_id = id(cl2)

        cl3 = cl1
        cl3 = cl1 - cl2

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(cl2, cl2_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(cl2), cl2_id)

    def test_add_list_not_modified(self):
        cl1 = CustomList([1, 2, 3])
        lst = [4, 5, 6]
        cl1_copy = cl1[:]
        lst_copy = lst[:]
        cl1_id = id(cl1)
        lst_id = id(lst)

        cl3 = cl1
        cl3 = cl1 + lst

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(lst, lst_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(lst), lst_id)

    def test_sub_list_not_modified(self):
        cl1 = CustomList([7, 8, 9])
        lst = [3, 2, 1]
        cl1_copy = cl1[:]
        lst_copy = lst[:]
        cl1_id = id(cl1)
        lst_id = id(lst)

        cl3 = cl1
        cl3 = cl1 - lst

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(lst, lst_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(lst), lst_id)

    def test_add_int_not_modified(self):
        cl1 = CustomList([1, 2, 3])
        cl1_copy = cl1[:]
        cl1_id = id(cl1)

        cl3 = cl1
        cl3 = cl1 + 10

        self.assertEqual(cl1, cl1_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)

    def test_sub_int_not_modified(self):
        cl1 = CustomList([7, 8, 9])
        cl1_copy = cl1[:]
        cl1_id = id(cl1)

        cl3 = cl1
        cl3 = cl1 - 5

        self.assertEqual(cl1, cl1_copy)
        self.assertNotEqual(cl3, cl1)
        self.assertEqual(id(cl1), cl1_id)

    def test_reverse_add_list_not_modified(self):
        lst = [4, 5, 6]
        cl1 = CustomList([1, 2, 3])
        cl1_copy = cl1[:]
        lst_copy = lst[:]
        cl1_id = id(cl1)
        lst_id = id(lst)

        _ = lst + cl1

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(lst, lst_copy)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(lst), lst_id)

    def test_reverse_sub_list_not_modified(self):
        lst = [4, 5, 6]
        cl1 = CustomList([7, 8, 9])
        cl1_copy = cl1[:]
        lst_copy = lst[:]
        cl1_id = id(cl1)
        lst_id = id(lst)

        _ = lst - cl1

        self.assertEqual(cl1, cl1_copy)
        self.assertEqual(lst, lst_copy)
        self.assertEqual(id(cl1), cl1_id)
        self.assertEqual(id(lst), lst_id)

    def test_add_custom_list_with_same_and_different_lengths(self):
        # Сложение с одинаковой длиной
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([4, 5, 6])
        expected_result_same_length = CustomList([5, 7, 9])
        result_same_length_left = cl1 + cl2
        result_same_length_right = cl2 + cl1

        self.assertEqual(result_same_length_left, result_same_length_right)

        self.assertEqual(type(result_same_length_left), CustomList)
        self.assertEqual(result_same_length_left, expected_result_same_length)
        self.assertEqual(type(result_same_length_right), CustomList)
        self.assertEqual(result_same_length_right, expected_result_same_length)

        # Сложение с разной длиной
        cl3 = CustomList([1, 2, 3, 4])
        cl4 = CustomList([5, 6])
        expected_result_different_length = CustomList([6, 8, 3, 4])
        result_different_length_left = cl3 + cl4
        result_different_length_rigth = cl4 + cl3

        self.assertEqual(
            result_different_length_left, result_different_length_rigth
        )
        self.assertEqual(type(result_different_length_left), CustomList)
        self.assertEqual(
            result_different_length_left, expected_result_different_length
        )
        self.assertEqual(type(result_different_length_rigth), CustomList)
        self.assertEqual(
            result_different_length_rigth, expected_result_different_length
        )

        # Сложение с пустым списком
        cl5 = CustomList([1, 2, 3, 4])
        cl6 = CustomList([])
        expected_result_empty_custom_list = CustomList([1, 2, 3, 4])
        result_empty_length_left = cl5 + cl6
        result_empty_length_rigth = cl6 + cl5

        self.assertEqual(result_empty_length_left, result_empty_length_rigth)
        self.assertEqual(type(result_empty_length_left), CustomList)
        self.assertEqual(
            result_empty_length_left, expected_result_empty_custom_list
        )
        self.assertEqual(type(result_empty_length_rigth), CustomList)
        self.assertEqual(
            result_empty_length_rigth, expected_result_empty_custom_list
        )

    def test_sub_custom_list_with_same_and_different_lengths(self):
        # Вычитание с одинаковой длиной
        cl1 = CustomList([10, 20, 30])
        cl2 = CustomList([1, 2, 3])
        expected_result_same_length = CustomList([9, 18, 27])
        result_same_length_left = cl1 - cl2
        result_same_length_right = cl2 - cl1

        self.assertEqual(result_same_length_left, expected_result_same_length)
        self.assertEqual(type(result_same_length_left), CustomList)
        self.assertEqual(result_same_length_right, CustomList([-9, -18, -27]))
        self.assertEqual(type(result_same_length_right), CustomList)

        # Вычитание с разной длиной
        cl3 = CustomList([10, 20, 30, 40])
        cl4 = CustomList([1, 2])
        expected_result_different_length = CustomList([9, 18, 30, 40])
        result_different_length_left = cl3 - cl4
        result_different_length_right = cl4 - cl3

        self.assertEqual(
            result_different_length_left, expected_result_different_length
        )
        self.assertEqual(type(result_different_length_left), CustomList)
        self.assertEqual(
            result_different_length_right, CustomList([-9, -18, -30, -40])
        )
        self.assertEqual(type(result_different_length_right), CustomList)

        # Вычитание с пустым списком
        cl3 = CustomList([10, 20, 30, 40])
        cl4 = CustomList([])
        expected_result_empty = CustomList([10, 20, 30, 40])
        result_empty_length_left = cl3 - cl4
        result_empty_length_right = cl4 - cl3

        self.assertEqual(result_empty_length_left, expected_result_empty)
        self.assertEqual(type(result_empty_length_left), CustomList)
        self.assertEqual(
            result_empty_length_right, CustomList([-10, -20, -30, -40])
        )
        self.assertEqual(type(result_empty_length_right), CustomList)

    def test_add_custom_list_with_list(self):
        # Сложение с одинаковой длиной
        cl1 = CustomList([1, 2, 3])
        list1 = [4, 5, 6]
        expected_result_same_length = CustomList([5, 7, 9])
        result_same_length_left = cl1 + list1
        result_same_length_right = list1 + cl1

        self.assertEqual(result_same_length_left, expected_result_same_length)
        self.assertEqual(type(result_same_length_left), CustomList)
        self.assertEqual(result_same_length_right, expected_result_same_length)
        self.assertEqual(type(result_same_length_right), CustomList)

        # Сложение с разной длиной
        cl2 = CustomList([1, 2, 3, 4])
        list2 = [5, 6]
        expected_result_different_length = CustomList([6, 8, 3, 4])
        result_different_length_left = cl2 + list2
        result_different_length_right = list2 + cl2

        self.assertEqual(
            result_different_length_left, expected_result_different_length
        )
        self.assertEqual(type(result_different_length_left), CustomList)
        self.assertEqual(
            result_different_length_right, expected_result_different_length
        )
        self.assertEqual(type(result_different_length_right), CustomList)

    def test_sub_custom_list_with_list(self):
        # Вычитание с одинаковой длиной
        cl1 = CustomList([10, 20, 30])
        list1 = [4, 5, 6]
        expected_result_same_length_left = CustomList([6, 15, 24])
        expected_result_same_length_right = CustomList([-6, -15, -24])
        result_same_length_left = cl1 - list1
        result_same_length_right = list1 - cl1

        self.assertEqual(
            result_same_length_left, expected_result_same_length_left
        )
        self.assertEqual(type(result_same_length_left), CustomList)
        self.assertEqual(
            result_same_length_right, expected_result_same_length_right
        )
        self.assertEqual(type(result_same_length_right), CustomList)

        # Вычитание с разной длиной
        cl2 = CustomList([10, 20, 30, 40])
        list2 = [5, 6]
        expected_result_different_length_left = CustomList([5, 14, 30, 40])
        expected_result_different_length_right = CustomList([-5, -14, -30, -40])
        result_different_length_left = cl2 - list2
        result_different_length_right = list2 - cl2

        self.assertEqual(
            result_different_length_left, expected_result_different_length_left
        )
        self.assertEqual(type(result_different_length_left), CustomList)
        self.assertEqual(
            result_different_length_right,
            expected_result_different_length_right,
        )
        self.assertEqual(type(result_different_length_right), CustomList)

    def test_add_custom_list_with_int(self):
        cl1 = CustomList([1, 2, 3])
        int_value = 5
        expected_result = CustomList([6, 7, 8])  # [1+5, 2+5, 3+5]

        # Проверка сложения CustomList + int
        result = cl1 + int_value
        self.assertEqual(result, expected_result)
        self.assertEqual(type(result), CustomList)

        # Проверка сложения int + CustomList
        result_reverse = int_value + cl1
        self.assertEqual(result_reverse, expected_result)
        self.assertEqual(type(result_reverse), CustomList)

    def test_sub_custom_list_with_int(self):
        cl1 = CustomList([10, 20, 30])
        int_value = 5
        expected_result = CustomList([5, 15, 25])  # [10-5, 20-5, 30-5]
        expected_result_reverse = CustomList(
            [-5, -15, -25]
        )  # [5-10, 5-20, 5-30]

        # Проверка вычитания CustomList - int
        result = cl1 - int_value
        self.assertEqual(result, expected_result)
        self.assertEqual(type(result), CustomList)

        # Проверка вычитания int - CustomList
        result_reverse = int_value - cl1
        self.assertEqual(result_reverse, expected_result_reverse)
        self.assertEqual(type(result_reverse), CustomList)

    def test_comparison_custom_lists(self):
        # Тесты сравнения
        cl1 = CustomList([1, 3, 3])
        cl2 = CustomList([3, 4, 5])
        cl3 = CustomList([1, 2, 4])

        self.assertTrue(cl1 < cl2)  # 6 < 12
        self.assertTrue(cl1 <= cl3)  # 6 <= 6
        self.assertTrue(cl1 == cl3)  # 6 == 6
        self.assertTrue(cl1 != cl2)  # 6 != 12
        self.assertTrue(cl2 > cl1)  # 12 > 6
        self.assertTrue(cl2 >= cl1)  # 12 >= 6

    def test_comparison_with_different_lengths(self):
        # Тесты сравнения с разными длинами
        cl1 = CustomList([1, 2])
        cl2 = CustomList([1, 2, 3, 4])

        self.assertTrue(cl1 < cl2)  # 3 < 10
        self.assertTrue(cl1 <= cl2)  # 3 <= 10
        self.assertFalse(cl2 < cl1)  # 10 !< 3
        self.assertFalse(cl1 == cl2)  # 3 != 10
        self.assertTrue(cl1 != cl2)  # 3 != 10

        cl3 = CustomList([10])
        cl4 = CustomList([1, 2, 3, 4])

        self.assertFalse(cl3 < cl4)
        self.assertTrue(cl3 <= cl4)
        self.assertTrue(cl3 >= cl4)
        self.assertFalse(cl3 < cl4)
        self.assertTrue(cl3 == cl4)
        self.assertFalse(cl3 != cl4)

    def test_invalid_type(self):
        # Проверка на ошибку при некорректных типах
        cl1 = CustomList([1, 2, 3])
        with self.assertRaises(ValueError):
            _ = cl1 + "string"
        with self.assertRaises(ValueError):
            _ = cl1 - None
        with self.assertRaises(ValueError):
            _ = 13.213 + cl1
        with self.assertRaises(ValueError):
            _ = "123" - cl1

    def test_str_method(self):
        cl = CustomList([1, 2, 3])
        expected_output = "CustomList([1, 2, 3]) with sum 6"
        self.assertEqual(str(cl), expected_output)

    def test_empty_list_str_method(self):
        cl_empty = CustomList([])
        expected_output_empty = "CustomList([]) with sum 0"
        self.assertEqual(str(cl_empty), expected_output_empty)

    def test_single_element_list_str_method(self):
        cl_single = CustomList([5])
        expected_output_single = "CustomList([5]) with sum 5"
        self.assertEqual(str(cl_single), expected_output_single)
