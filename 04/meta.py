"Homework 4 with CustomMeta class"


class CustomMeta(type):
    "Meta class that customize attrs name"

    def __new__(mcs, name, bases, classdict):
        def get_new_key(key):
            return (
                key if key.startswith("__") and key.endswith("__") else "custom_" + key
            )

        custom_classdict = {get_new_key(key): classdict[key] for key in classdict}
        cls = super().__new__(mcs, name, bases, custom_classdict)

        def custom_setattr(setattr):  # pylint: disable=redefined-builtin
            def wrapper(self, name, value):
                return setattr(self, "custom_" + name, value)

            return wrapper

        cls.__setattr__ = custom_setattr(cls.__setattr__)
        return cls

    def __setattr__(cls, name, value):
        custom_name = (
            name if name.startswith("__") and name.endswith("__") else "custom_" + name
        )
        return super().__setattr__(custom_name, value)


class CustomClass(metaclass=CustomMeta):
    "Class for tests"

    x = 10
    _y = 20

    def __init__(self, val=99):
        self.val = val

    def line(self):
        "Test func"

        return 100

    def __str__(self):
        return "Custom_by_metaclass"
