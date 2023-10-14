"Homework 4 with descriptors"


class Float:
    "Float descriptor accepts only numbers to set"

    def __set_name__(self, _, name):
        self.name = f"_float_descr_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, (int, float)):
            raise ValueError

        return setattr(obj, self.name, val)

    def __get__(self, obj, _):
        if obj is None:
            return None

        return getattr(obj, self.name)


class PositiveInteger:
    "PositiveInteger descriptor allows to contain only positive integers"

    def __set_name__(self, _, name):
        self.name = f"_posint_descr_{name}"

    def __set__(self, obj, val):
        if not isinstance(val, int):
            raise ValueError

        if val <= 0:
            raise ValueError

        return setattr(obj, self.name, val)

    def __get__(self, obj, _):
        if obj is None:
            return None

        return getattr(obj, self.name)


class String:
    "String descriptor allows to set only once"
    __setted = set()

    def __set_name__(self, _, name):
        self.name = f"_str_descr_{name}"

    def __set__(self, obj, val):
        if obj in self._String__setted:
            raise AttributeError

        if not isinstance(val, str):
            raise ValueError

        self._String__setted.add(obj)

        return setattr(obj, self.name, val)

    def __get__(self, obj, _):
        if obj is None:
            return None

        return getattr(obj, self.name)


class Civilization:
    "Class Civilization to test descriptors"

    name = String()
    cities = PositiveInteger()
    gold = Float()

    def __init__(self, name):
        self.name = name
        self.cities = 1
        self.gold = 0

    def build_city(self):
        "Civ builds new city"

        self.cities += 1

    def earn(self, amount):
        "Civ erans some gold"

        self.gold += amount

    def spend(self, amount):
        "Civ spends some gold"

        self.gold -= amount
