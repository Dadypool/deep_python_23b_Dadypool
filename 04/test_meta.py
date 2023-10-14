"Homework 4 with tests for CustomMeta class"

from unittest import TestCase

from meta import CustomMeta, CustomClass


class TestMeta(TestCase):
    "Class with tests"

    def test_cls_attrs(self):
        "Tests class attributes from CustomClass"

        self.assertEqual(CustomClass.custom_x, 10)
        with self.assertRaises(AttributeError):
            getattr(CustomClass, "x")

        self.assertEqual(CustomClass.custom__y, 20)
        with self.assertRaises(AttributeError):
            getattr(CustomClass, "_y")

    def test_insts_attrs(self):
        "Tests class attributes from class instances"

        inst = CustomClass()
        self.assertEqual(inst.custom_val, 99)
        with self.assertRaises(AttributeError):
            getattr(inst, "val")

        inst = CustomClass(10)
        self.assertEqual(inst.custom_val, 10)
        with self.assertRaises(AttributeError):
            getattr(inst, "val")

        self.assertEqual(inst.custom_x, 10)
        with self.assertRaises(AttributeError):
            getattr(inst, "x")

        self.assertEqual(inst.custom__y, 20)
        with self.assertRaises(AttributeError):
            getattr(inst, "_y")

        self.assertEqual(inst.custom_line(), 100)
        with self.assertRaises(AttributeError):
            inst.line()

        self.assertEqual(str(inst), "Custom_by_metaclass")

    def test_new_cls_attrs(self):
        "Tests class attributes from new class of CustomMeta metaclass"

        custom_class = CustomMeta("Custom", (), {"x": 1, "_y": 2, "__z": 3})
        custom_class.__w = 4

        self.assertEqual(custom_class.custom_x, 1)
        with self.assertRaises(AttributeError):
            getattr(custom_class, "x")

        self.assertEqual(custom_class.custom__y, 2)
        with self.assertRaises(AttributeError):
            getattr(custom_class, "_y")

        self.assertEqual(custom_class.custom___z, 3)
        with self.assertRaises(AttributeError):
            getattr(custom_class, "__z")

        self.assertEqual(custom_class.custom__TestMeta__w, 4)
        with self.assertRaises(AttributeError):
            getattr(custom_class, "__w")

        with self.assertRaises(AttributeError):
            getattr(custom_class, "custom___init___")

    def test_inst_attrs_of_new_cls(self):
        "Tests class attributes from new class instances"

        custom_class = CustomMeta("Custom", (), {"x": 1, "_y": 2, "__z": 3})
        inst = custom_class()

        self.assertEqual(inst.custom_x, 1)
        with self.assertRaises(AttributeError):
            getattr(inst, "x")

        self.assertEqual(inst.custom__y, 2)
        with self.assertRaises(AttributeError):
            getattr(inst, "_y")

        self.assertEqual(inst.custom___z, 3)
        with self.assertRaises(AttributeError):
            getattr(inst, "__z")

    def test_dyn_attrs(self):
        "Tests new class attributes added dynamically"

        inst = CustomClass()
        inst.dyn = "added later"

        self.assertEqual(inst.custom_dyn, "added later")
        with self.assertRaises(AttributeError):
            getattr(inst, "dyn")

        CustomClass.cls_dyn = "added later to class"
        self.assertEqual(CustomClass.custom_cls_dyn, "added later to class")
        with self.assertRaises(AttributeError):
            getattr(CustomClass, "cls_dyn")

        custom_class = CustomMeta("Custom", (), {})
        inst = custom_class()

        custom_class.cls_dyn = 1
        self.assertEqual(custom_class.custom_cls_dyn, 1)
        with self.assertRaises(AttributeError):
            getattr(inst, "cls_dyn")

        inst.dyn = 2
        self.assertEqual(inst.custom_dyn, 2)
        with self.assertRaises(AttributeError):
            getattr(inst, "dyn")
        self.assertEqual(inst.custom_cls_dyn, 1)
        with self.assertRaises(AttributeError):
            getattr(inst, "cls_dyn")
