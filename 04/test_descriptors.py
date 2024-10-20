import unittest
from .descriptors import MLModel, BaseDescriptor


class TestMLModel(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    def test_valid_model(self):
        """
        Тест на создание модели с корректными значениями
        """
        model = MLModel(feature_count=10, label="spam", learning_rate=0.05)
        self.assertEqual(model.feature_count, 10)
        self.assertEqual(model.label, "spam")
        self.assertEqual(model.learning_rate, 0.05)

    def test_valid_model_with_float_learning_rate(self):
        """
        Тест на создание модели с вещественной скоростью обучения
        """
        model = MLModel(feature_count=5, label="ham", learning_rate=0.1)
        self.assertEqual(model.learning_rate, 0.1)

    def test_valid_model_with_integer_learning_rate(self):
        """
        Тест на создание модели с целочисленной скоростью обучения
        """
        model = MLModel(feature_count=3, label="neutral", learning_rate=1)
        self.assertEqual(model.learning_rate, 1)

    def test_valid_model_with_large_feature_count(self):
        """
        Тест на создание модели с большим количеством признаков
        """
        model = MLModel(
            feature_count=10000, label="complex", learning_rate=0.01
        )
        self.assertEqual(model.feature_count, 10000)

    def test_feature_count_as_string(self):
        """
        Тест, что возникает ошибка,
        если количество признаков передается как строка
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count="10", label="valid", learning_rate=0.1)
        self.assertEqual(
            str(context.exception), "feature_count должен быть целым числом."
        )

    def test_valid_model_with_special_characters_in_label(self):
        """
        Тест на создание модели с меткой, содержащей специальные символы
        """
        model = MLModel(feature_count=8, label="spam@123", learning_rate=0.3)
        self.assertEqual(model.label, "spam@123")

    def test_valid_model_with_decimal_learning_rate(self):
        """
        Тест на создание модели с десятичной скоростью обучения
        """
        model = MLModel(feature_count=12, label="test", learning_rate=0.3333)
        self.assertEqual(model.learning_rate, 0.3333)

    def test_learning_rate_as_string(self):
        """
        Тест, что возникает ошибка, если скорость обучения передается как строка
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate="0.1")
        self.assertEqual(
            str(context.exception), "learning_rate должен быть числом."
        )

    def test_feature_count_zero(self):
        """
        Тест, что возникает ошибка при нулевом количестве признаков
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=0, label="test", learning_rate=0.5)
        self.assertEqual(
            str(context.exception),
            "feature_count должен быть положительным целым числом.",
        )

    def test_feature_count_negative(self):
        """
        Тест, что возникает ошибка при отрицательном количестве признаков
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=-1, label="test", learning_rate=0.5)
        self.assertEqual(
            str(context.exception),
            "feature_count должен быть положительным целым числом.",
        )

    def test_label_with_whitespace(self):
        """
        Тест, что возникает ошибка, если метка состоит только из пробелов.
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="   ", learning_rate=0.5)
        self.assertEqual(str(context.exception), "label не может быть пустым.")

    def test_label_empty(self):
        """
        Тест, что возникает ошибка при пустой метке
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="", learning_rate=0.5)
        self.assertEqual(str(context.exception), "label не может быть пустым.")

    def test_label_none(self):
        """
        Тест, что возникает ошибка при метке, равной None
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label=None, learning_rate=0.5)
        self.assertEqual(str(context.exception), "label должен быть строкой.")

    def test_learning_rate_too_high(self):
        """
        Тест, что возникает ошибка при слишком высокой скорости обучения
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate=1.5)
        self.assertEqual(
            str(context.exception),
            "learning_rate должен быть в пределах от 0 до 1.",
        )

    def test_learning_rate_negative(self):
        """
        Тест, что возникает ошибка при отрицательной скорости обучения
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate=-0.1)
        self.assertEqual(
            str(context.exception),
            "learning_rate должен быть в пределах от 0 до 1.",
        )

    def test_learning_rate_incorrect_values(self):
        """
        Тест, что возникает ошибка при неккоректных значениях скорости обучения
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate=0)
        self.assertEqual(
            str(context.exception),
            "learning_rate должен быть в пределах от 0 до 1.",
        )

        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate=1.1)
        self.assertEqual(
            str(context.exception),
            "learning_rate должен быть в пределах от 0 до 1.",
        )

    def test_learning_rate_as_list(self):
        """
        Тест, что возникает ошибка, если скорость обучения передается как список
        """
        with self.assertRaises(ValueError) as context:
            MLModel(feature_count=5, label="valid", learning_rate=[0.1])
        self.assertEqual(
            str(context.exception), "learning_rate должен быть числом."
        )

    def test_feature_count_validate_not_implemented(self):
        """
        Тест, что метод validate в BaseDescriptor вызывает NotImplementedError.
        """

        class IncompleteClass(BaseDescriptor):  # pylint: disable=W0223,R0903
            pass

        with self.assertRaises(NotImplementedError) as context:
            BaseDescriptor().validate(object)
        self.assertEqual(
            str(context.exception), "Подклассы должны реализовать этот метод."
        )

        with self.assertRaises(NotImplementedError) as context:
            IncompleteClass().validate(object)
        self.assertEqual(
            str(context.exception), "Подклассы должны реализовать этот метод."
        )
