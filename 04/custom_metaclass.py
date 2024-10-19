class CustomMeta(type):
    """
    Метакласс, который добавляет префикс 'custom_' к атрибутам класса
    и экземпляра, если они не являются магическими методами.

    Атрибуты:
        mcs: Метакласс.
        name: Имя создаваемого класса.
        bases: Кортеж базовых классов.
        dct: Словарь атрибутов и методов класса.

    Методы:
        __new__(mcs, name, bases, dct):
            Создает новый класс с измененными атрибутами.

        __init__(cls, name, bases, dct):
            Настраивает поведение установки атрибутов экземпляров.
    """

    def __new__(mcs, name, bases, dct):
        new_dct = {
            (
                f"custom_{key}"
                if not (key.startswith("__") and key.endswith("__"))
                else key
            ): value
            for key, value in dct.items()
        }

        cls = super().__new__(mcs, name, bases, new_dct)
        return cls

    def __init__(cls, name, bases, dct):
        original_setattr = cls.__setattr__

        def __setattr__(self, name, value):
            name = (
                f"custom_{name}"
                if not (name.startswith("__") and name.endswith("__"))
                else name
            )
            return original_setattr(self, name, value)

        cls.__setattr__ = __setattr__
        super().__init__(name, bases, dct)


# pylint: disable=C0115,C0116
class CustomClass(metaclass=CustomMeta):
    x: int = 50

    def __init__(self, val=99) -> None:
        self.val = val

    def line(self) -> int:
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
