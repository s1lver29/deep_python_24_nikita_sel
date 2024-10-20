# pylint: disable=R0903


class BaseDescriptor:
    def __init__(self):
        self.owner = None
        self.name = None

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        raise NotImplementedError("Подклассы должны реализовать этот метод.")


class FeatureCount(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.name} должен быть целым числом.")
        if value <= 0:
            raise ValueError(
                f"{self.name} должен быть положительным целым числом."
            )


class Label(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} должен быть строкой.")
        if not value.strip():
            raise ValueError(f"{self.name} не может быть пустым.")


class LearningRate(BaseDescriptor):
    def validate(self, value):
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
