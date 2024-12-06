# pylint: disable=R0903
from abc import ABC, abstractmethod


class BaseDescriptor(ABC):
    def __init__(self):
        self.name = None
        self.private_name = None

    def __set_name__(self, owner, name) -> None:
        self.name = name
        self.private_name = f"_{name}"

    def __set__(self, instance, value) -> None:
        self.validate(value)
        setattr(instance, self.private_name, value)

    def __get__(self, instance, owner) -> object:
        return getattr(instance, self.private_name, None)

    @abstractmethod
    def validate(self, value):
        pass


class FeatureCount(BaseDescriptor):
    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(f"{self.name} должен быть целым числом.")
        if value <= 0:
            raise ValueError(
                f"{self.name} должен быть положительным целым числом."
            )


class Label(BaseDescriptor):
    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{self.name} должен быть строкой.")
        if not value.strip():
            raise ValueError(f"{self.name} не может быть пустым.")


class LearningRate(BaseDescriptor):
    def validate(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise ValueError(f"{self.name} должен быть числом.")
        if value <= 0 or value > 1:
            raise ValueError(f"{self.name} должен быть в пределах от 0 до 1.")


class MLModel:
    feature_count = FeatureCount()
    label = Label()
    learning_rate = LearningRate()

    def __init__(self, feature_count, label, learning_rate):
        self.feature_count = feature_count
        self.label = label
        self.learning_rate = learning_rate
