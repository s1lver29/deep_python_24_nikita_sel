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

        true_message_called = "чапаев и пустота"
        mock_predict.assert_called_with(message=true_message_called)

    @patch.object(SomeModel, "predict")
    def test_bad_message(self, mock_predict):
        """
        bad_threshold дефолтное значение
        Проверка, если сообщения меньше bad_threshold
        """
        mock_predict.return_value = 0.1

        pred = predict_message_mood("Вулкан")
        self.assertEqual(pred, "неуд")

        true_message_called = "вулкан"
        mock_predict.assert_called_with(message=true_message_called)

    @patch.object(SomeModel, "predict")
    def test_normal_message(self, mock_predict):
        """
        [bad_threshold; good_threshold] дефолтные значения
        Проверка, если значение в районе [bad_threshold; good_threshold]
        """
        mock_predict.return_value = 0.5

        pred = predict_message_mood("Нормально")
        self.assertEqual(pred, "норм")

        true_message_called = "нормально"
        mock_predict.assert_called_with(message=true_message_called)

    def test_empty_message(self):
        """
        Проверка, если сообщение пустое, то возвратом будет ошибка,
        что строка пустая
        """
        with self.assertRaises(ValueError):
            predict_message_mood("")
        with self.assertRaises(ValueError):
            predict_message_mood(" " * 10)

    def test_incorrect_thresholds(self):
        """
        Проверка, что bad_thresholds и good_thresholds некорректные
        """
        invalid_thresholds = [
            (0.5, None),
            (None, 1),
            (-0.5, 0.9),
            (1.5, 0.9),
            (0.5, -0.9),
            (0.5, 1.9),
            (0.9, 0.5),
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
    def test_incorrect_answer_models(self, mock_predict):
        """
        Проверка, что из модели возвращаются не вероятности от 0 до 1
        """
        invalid_outputs = [123, -1, -0.001, 1.0001]
        for invalid in invalid_outputs:
            mock_predict.return_value = invalid
            with self.assertRaises(ValueError):
                predict_message_mood(
                    message=self.valid_message,
                    bad_thresholds=0.1,
                    good_thresholds=0.9,
                )

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

    @patch.object(SomeModel, "predict")
    def test_boundary_values(self, mock_predict):
        """
        Проверка граничных значений для bad_threshold и good_threshold
        """
        # Проверяем случай, когда предсказание равно bad_threshold
        mock_predict.return_value = 0.3
        pred = predict_message_mood(
            "Граничное значение", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="граничное значение")

        # Проверяем случай, когда предсказание чуть меньше bad_threshold
        mock_predict.return_value = 0.299
        pred = predict_message_mood(
            "Чуть ниже порога", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "неуд")
        mock_predict.assert_called_with(message="чуть ниже порога")

        # Проверяем случай, когда предсказание чуть больше bad_threshold
        mock_predict.return_value = 0.301
        pred = predict_message_mood(
            "Чуть выше порога", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="чуть выше порога")

        # Проверяем случай, когда предсказание равно good_threshold
        mock_predict.return_value = 0.8
        pred = predict_message_mood(
            "Граничное значение", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="граничное значение")

        # Проверяем случай, когда предсказание чуть меньше good_threshold
        mock_predict.return_value = 0.799
        pred = predict_message_mood(
            "Чуть ниже порога", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="чуть ниже порога")

        # Проверяем случай, когда предсказание чуть больше good_threshold
        mock_predict.return_value = 0.801
        pred = predict_message_mood(
            "Чуть выше порога", bad_thresholds=0.3, good_thresholds=0.8
        )
        self.assertEqual(pred, "отл")
        mock_predict.assert_called_with(message="чуть выше порога")

    @patch.object(SomeModel, "predict")
    def test_boundary_thresholds_and_values(self, mock_predict):
        """
        Проверка граничных значений для bad_threshold и good_threshold
        при различных краевых случаях
        """
        # Максимальные трешхолды
        max_bad_thresholds, max_good_thresholds = 1, 1

        # Значение предикта равно границам
        mock_predict.return_value = 1
        pred = predict_message_mood(
            "Граничное значение",
            bad_thresholds=max_bad_thresholds,
            good_thresholds=max_good_thresholds,
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="граничное значение")

        # Значение предикта меньше
        mock_predict.return_value = 0.9
        pred = predict_message_mood(
            "Ниже порога",
            bad_thresholds=max_bad_thresholds,
            good_thresholds=max_good_thresholds,
        )
        self.assertEqual(pred, "неуд")
        mock_predict.assert_called_with(message="ниже порога")

        # Минимальные трешхолды
        min_bad_thresholds, min_good_thresholds = 0, 0

        # Значение предикта равно границам
        mock_predict.return_value = 0
        pred = predict_message_mood(
            "Граничное значение",
            bad_thresholds=min_bad_thresholds,
            good_thresholds=min_good_thresholds,
        )
        self.assertEqual(pred, "норм")
        mock_predict.assert_called_with(message="граничное значение")

        # Значение предикта меньше
        mock_predict.return_value = 0.1
        pred = predict_message_mood(
            "Выше порога",
            bad_thresholds=min_bad_thresholds,
            good_thresholds=min_good_thresholds,
        )
        self.assertEqual(pred, "отл")
        mock_predict.assert_called_with(message="выше порога")
