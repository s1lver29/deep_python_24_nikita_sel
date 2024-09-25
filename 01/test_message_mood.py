import unittest
from unittest.mock import patch

from .message_mood import predict_message_mood, SomeModel


class TestPredMessageMood(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_message = "message"  # Валидное значение
        print(f"\nStart test {self.id()}")

    def tearDown(self) -> None:
        print(f"End test {self.id()}")

    @patch.object(SomeModel, "predict")
    def test_good_message(self, mock_predict):
        """
        good_threshold дефолтное значение
        Проверка, если сообщение больше good_threshold
        """
        mock_predict.return_value = 0.9

        pred = predict_message_mood("Чапаев и пустота")
        self.assertEqual(pred, "отл")

    @patch.object(SomeModel, "predict")
    def test_bad_message(self, mock_predict):
        """
        bad_threshold дефолтное значение
        Проверка, если сообщения меньше bad_threshold
        """
        mock_predict.return_value = 0.1

        pred = predict_message_mood("Вулкан")
        self.assertEqual(pred, "неуд")

    @patch.object(SomeModel, "predict")
    def test_normal_message(self, mock_predict):
        """
        [bad_threshold; good_threshold] дефолтные значения
        Проверка, если значение в районе [bad_threshold; good_threshold]
        """
        mock_predict.return_value = 0.5

        pred = predict_message_mood("Нормально")
        self.assertEqual(pred, "норм")

    def test_empty_message(self):
        """
        Проверка, если сообщение пустое, то возвратом будет ошибка,
        что строка пустая
        """
        with self.assertRaises(ValueError):
            predict_message_mood("")

    def test_incorrect_thresholds(self):
        """
        Проверка, что bad_thresholds и good_thresholds некорректные
        """
        invalid_thresholds = [
            (-1, None),
            (2, None),
            (None, -1),
            (None, 2),
            (1, 0.5),
        ]
        for bad, good in invalid_thresholds:
            with self.assertRaises((ValueError, TypeError)):
                predict_message_mood(
                    message=self.valid_message,
                    bad_thresholds=bad,
                    good_thresholds=good,
                )

    def test_message_is_not_string(self):
        """
        Проверка, что message не строка
        """
        invalid_inputs = [123, None, [], {}, 45.67, object()]
        for invalid in invalid_inputs:
            with self.assertRaises(TypeError):
                predict_message_mood(message=invalid)

    @patch.object(SomeModel, "predict")
    def test_valid_equal_thresholds(self, mock_predict):
        """
        Проверка, что при равенстве bad_thresholds и good_thresholds
        отрабатывать будет корректно
        """
        test_cases = [
            (0.5, 0.5, 0.49, "неуд"),
            (0.5, 0.5, 0.5, "норм"),
            (0.5, 0.5, 0.51, "отл"),
        ]
        for (
            bad_thresholds,
            good_thresholds,
            model_prediction,
            expected,
        ) in test_cases:
            mock_predict.return_value = model_prediction

            result = predict_message_mood(
                "Тестовое сообщение",
                bad_thresholds=bad_thresholds,
                good_thresholds=good_thresholds,
            )
            self.assertEqual(result, expected)
