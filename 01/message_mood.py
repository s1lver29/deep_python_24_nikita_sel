class SomeModel:
    # pylint: disable=too-few-public-methods
    def predict(self, message: str) -> float:
        pass


def predict_message_mood(
    message: str, bad_thresholds: float = 0.3, good_thresholds: float = 0.8
) -> str:
    if not isinstance(message, str):
        raise TypeError(
            f"Получено {type(message).__name__}. "
            "message должна быть строкой (str)."
        )
    if not message.strip():
        raise ValueError("Ожидалось, что message не пустая строка.")
    if not 0 <= bad_thresholds <= 1:
        raise ValueError(
            f"Получено {bad_thresholds=}. "
            "Значение bad_thresholds лежит от (0, 1)."
        )
    if not 0 <= good_thresholds <= 1:
        raise ValueError(
            f"Получено {good_thresholds=}. "
            "Значение good_thresholds лежит (0, 1)."
        )
    if bad_thresholds > good_thresholds:
        raise ValueError(
            "bad_thresholds должен быть меньше или равен good_thresholds."
        )

    model = SomeModel()
    pred = model.predict(message=message.lower())  # pylint: disable=E1111

    if pred > good_thresholds:
        return "отл"
    if pred < bad_thresholds:
        return "неуд"
    return "норм"
