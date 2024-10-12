from typing import Union
from itertools import zip_longest


class CustomList(list):
    def __add_lists(
        self, other: Union[list[int], "CustomList"]
    ) -> "CustomList":
        return CustomList(
            self_value + other_value
            for self_value, other_value in zip_longest(self, other, fillvalue=0)
        )

    def __sub_lists(
        self, other: Union[list[int], "CustomList"]
    ) -> "CustomList":
        return CustomList(
            self_value - other_value
            for self_value, other_value in zip_longest(self, other, fillvalue=0)
        )

    def __add__(
        self, other: Union[int, list[int], "CustomList"]
    ) -> "CustomList":
        if isinstance(other, int):
            other = [other] * len(self)
        if isinstance(other, (CustomList, list)):
            return self.__add_lists(other)

        raise ValueError(
            f"Получено {other=}. А надо list[int] | int | CustomList"
        )

    def __radd__(
        self, other: Union[list[int], int, "CustomList"]
    ) -> "CustomList":
        if isinstance(other, int):
            other = [other] * len(self)
        if isinstance(other, (list, CustomList)):
            return self.__add_lists(other)

        raise ValueError(
            f"Получено {other=}. А надо list[int] | int | CustomList"
        )

    def __sub__(
        self, other: Union[list[int], int, "CustomList"]
    ) -> "CustomList":
        if isinstance(other, int):
            other = [other] * len(self)
        if isinstance(other, (list, CustomList)):
            return self.__sub_lists(other)

        raise ValueError(
            f"Получено {other=}. А надо list[int] | int | CustomList"
        )

    def __rsub__(self, other):
        if isinstance(other, int):
            other = [other] * len(self)
        if isinstance(other, (list, CustomList)):
            return self.__sub_lists(other)

        raise ValueError(
            f"Получено {other=}. А надо list[int] | int | CustomList"
        )

    def __lt__(self, other: "CustomList") -> bool:
        return sum(self) < sum(other)

    def __le__(self, other: "CustomList") -> bool:
        return sum(self) <= sum(other)

    def __eq__(self, other: "CustomList") -> bool:
        return sum(self) == sum(other)

    def __ne__(self, other: "CustomList") -> bool:
        return sum(self) != sum(other)

    def __gt__(self, other: "CustomList") -> bool:
        return sum(self) > sum(other)

    def __ge__(self, other: "CustomList") -> bool:
        return sum(self) >= sum(other)
