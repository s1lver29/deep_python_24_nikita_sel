# pylint: skip-file
import unittest
from .custom_metaclass import CustomClass, CustomMeta


class TestCustomMeta(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_class_attributes(self):
        """
        Проверяет, что класс имеет атрибут с префиксом 'custom_'
        и недоступен обычный атрибут.
        """
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            CustomClass.x

    def test_instance_attributes(self):
        """
        Проверяет, что экземпляр класса имеет атрибут с префиксом 'custom_'
        и недоступен обычный атрибут.
        """
        inst = CustomClass()
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()

    def test_dynamic_attributes(self):
        """
        Проверяет, что динамически добавленный атрибут у экземпляра
        имеет префикс 'custom_'.
        """
        inst = CustomClass()
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            inst.dynamic

    def test_magic_methods_inheriting(self):
        """
        Проверяет, что магические методы не изменяются
        при использовании метакласса
        """

        class BaseClass:
            def func(self):
                pass

        class BaseClassWithMetaClass(metaclass=CustomMeta):
            def func(self):
                pass

        magic_methods = {
            method
            for method in dir(BaseClass)
            if method.startswith("__") and method.endswith("__")
        }
        derived_magic_methods = {
            method
            for method in dir(BaseClassWithMetaClass)
            if method.startswith("__") and method.endswith("__")
        }

        base_func = [
            func_name
            for func_name in BaseClass.__dict__.keys()
            if func_name.find("func")
        ]
        meta_func = [
            func_name
            for func_name in BaseClassWithMetaClass.__dict__.keys()
            if func_name.find("func")
        ]

        self.assertEqual(magic_methods, derived_magic_methods)
        self.assertNotEqual(base_func, meta_func)

    def test_multiple_classes(self):
        """
        Проверяет, что разные классы имеют свои собственные атрибуты
        и не пересекаются.
        """

        class CustomClass2(metaclass=CustomMeta):
            x: int = 100

        self.assertEqual(CustomClass.custom_x, 50)
        self.assertEqual(CustomClass2.custom_x, 100)
        self.assertNotEqual(id(CustomClass), id(CustomClass2))
        with self.assertRaises(AttributeError):
            CustomClass.custom_y
        with self.assertRaises(AttributeError):
            CustomClass2.custom_val

    def test_protected_and_private_attributes(self):
        """
        Проверяет, что защищенные и приватные атрибуты переименовываются
        и доступны через 'custom_'.
        """

        class CustomClassWithProtectedAndPrivate(metaclass=CustomMeta):
            def __init__(self):
                self._protected_attr = "protected"
                self.__private_attr = "private"

        inst = CustomClassWithProtectedAndPrivate()
        self.assertEqual(inst.custom__protected_attr, "protected")
        self.assertEqual(
            inst.custom__CustomClassWithProtectedAndPrivate__private_attr,
            "private",
        )
        with self.assertRaises(AttributeError):
            inst._protected_attr
        with self.assertRaises(AttributeError):
            inst._CustomClassWithProtectedAndPrivate__private_attr

    def test_non_public_methods(self):
        """
        Проверяет, что защищенные и приватные методы переименовываются
        и доступны через 'custom_'.
        """

        class CustomClassWithNonPublicMethods(metaclass=CustomMeta):
            def __private_method(self) -> str:
                return "private"

            def _protected_method(self) -> str:
                return "protected"

        inst = CustomClassWithNonPublicMethods()
        self.assertEqual(inst.custom__protected_method(), "protected")
        self.assertEqual(
            inst.custom__CustomClassWithNonPublicMethods__private_method(),
            "private",
        )
        with self.assertRaises(AttributeError):
            inst._CustomClassWithNonPublicMethods__private_method()
        with self.assertRaises(AttributeError):
            inst._protected_method()

    def test_class_dict(self):
        """
        Проверяет, что атрибут с префиксом 'custom_'
        присутствует в __dict__ класса.
        """

        class CustomClass3(metaclass=CustomMeta):
            z = 200

        self.assertIn("custom_z", CustomClass3.__dict__)
        self.assertEqual(CustomClass3.custom_z, 200)
        with self.assertRaises(AttributeError):
            CustomClass3.z

    def test_magic_methods(self):
        """
        Проверяет, что магические методы присутствуют в классе
        и работают корректно.
        """
        self.assertIn("__init__", CustomClass.__dict__)
        self.assertIn("__str__", CustomClass.__dict__)

        inst = CustomClass()
        self.assertEqual(str(inst), "Custom_by_metaclass")
        self.assertEqual(inst.__class__, CustomClass)
