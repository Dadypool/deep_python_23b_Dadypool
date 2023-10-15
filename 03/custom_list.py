"Homework 3 with custom list class"

from collections.abc import Iterable
from math import isclose


class CustomList(list):
    "class with custom list behavior"

    def __add__(self, other: list) -> "CustomList":
        if not isinstance(other, list):
            raise TypeError(
                "CustomLists support add and sub operations only with lists"
            )

        changed = False
        more, less = len(self), len(other)
        if len(self) < len(other):
            more, less = less, more
            changed = True

        ret_list = [0] * more
        for i in range(less):
            ret_list[i] = self[i] + other[i]
        for i in range(less, more):
            if changed:
                ret_list[i] = other[i]
            else:
                ret_list[i] = self[i]

        return CustomList(ret_list)

    def __radd__(self, other: list) -> "CustomList":
        return self.__add__(other)

    def __sub__(self, other: list) -> "CustomList":
        return self.__add__([-1 * el for el in other])

    def __rsub__(self, other: list) -> "CustomList":
        inv_self = CustomList([-1 * i for i in self])
        return inv_self.__add__(other)

    def __lt__(self, other: "CustomList") -> bool:
        if not isinstance(other, CustomList):
            raise TypeError("CustomList can be compared only with another CustomList")
        return sum(self) < sum(other)

    def __le__(self, other: "CustomList") -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: "CustomList") -> bool:
        if not isinstance(other, CustomList):
            raise TypeError("CustomList can be compared only with another CustomList")
        return isclose(sum(self), sum(other))

    def __ne__(self, other: "CustomList") -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: "CustomList") -> bool:
        if not isinstance(other, CustomList):
            raise TypeError("CustomList can be compared only with another CustomList")
        return sum(self) > sum(other)

    def __ge__(self, other: "CustomList") -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __str__(self):
        return super().__repr__() + f"  Sum: {sum(self)}"

    def __repr__(self):
        return f"CustomList({super().__repr__()})"
