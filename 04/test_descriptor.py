"Homework 4 with tests for descriptors"

from unittest import TestCase

from descriptor import Civilization


class TestDescriptor(TestCase):
    "Class with tests"

    def test_float_descr(self):
        "Tests Float descriptor"

        civ = Civilization("Rome")
        self.assertEqual(0, civ.gold)
        civ.earn(100)
        self.assertEqual(100, civ.gold)
        civ.spend(200.10)
        self.assertAlmostEqual(-100.1, civ.gold)
        civ.gold = 50
        self.assertAlmostEqual(50, civ.__dict__["_float_descr_gold"])

        with self.assertRaises(KeyError):
            assert civ.__dict__["gold"]
        with self.assertRaises(ValueError):
            civ.gold = "gold"
        self.assertEqual(50, civ.gold)
        self.assertIsNone(Civilization.gold)

    def test_posint_descr(self):
        "Tests PositiveInteger descriptor"

        civ = Civilization("China")
        self.assertEqual(1, civ.cities)
        civ.build_city()
        self.assertEqual(2, civ.cities)
        civ.cities = 10
        self.assertEqual(10, civ.cities)
        self.assertEqual(10, civ.__dict__["_posint_descr_cities"])

        with self.assertRaises(ValueError):
            civ.cities = 0
        with self.assertRaises(ValueError):
            civ.cities = -11

        with self.assertRaises(KeyError):
            assert civ.__dict__["cities"]
        with self.assertRaises(ValueError):
            civ.cities = "city"
        self.assertEqual(10, civ.cities)
        self.assertIsNone(Civilization.cities)

    def test_string_descr(self):
        "Tests String descriptor that can set only once"

        civ = Civilization("Greece")

        self.assertEqual("Greece", civ.name)
        self.assertEqual("Greece", civ.__dict__["_str_descr_name"])

        with self.assertRaises(KeyError):
            assert civ.__dict__["name"]
        with self.assertRaises(ValueError):
            civ = Civilization(7)
        with self.assertRaises(AttributeError):
            civ.name = "Macedonia"
        self.assertEqual("Greece", civ.name)
        self.assertIsNone(Civilization.name)

    def test_several_instances(self):
        "Tests descriptors work with several objects"

        france = Civilization("France")
        france.cities = 40
        france.gold = 4

        england = Civilization("England")
        england.cities = 10
        england.gold = 200

        self.assertEqual("England", england.name)
        self.assertEqual("France", france.name)

        self.assertEqual(10, england.cities)
        self.assertEqual(40, france.cities)

        england.build_city()
        france.build_city()
        self.assertEqual(11, england.cities)
        self.assertEqual(41, france.cities)

        self.assertEqual(200, england.gold)
        self.assertEqual(4, france.gold)

        with self.assertRaises(AttributeError):
            england.name = "GreatBritain"
        self.assertEqual("England", england.name)
        with self.assertRaises(AttributeError):
            france.name = "French Empire"
        self.assertEqual("France", france.name)
    
    def test_value_didnt_change_if_invalid(self):
        "Tests that atrributes value didn't change after set with invalid value"

        civ = Civilization("Carthage")
        civ.build_city()
        civ.earn(100)
        
        self.assertEqual("Carthage", civ.name)
        with self.assertRaises(AttributeError):
            civ.name = "Carthago delenda est"
        self.assertEqual("Carthage", civ.name)

        self.assertEqual(2, civ.cities)
        with self.assertRaises(ValueError):
            civ.cities = "many"
        self.assertEqual(2, civ.cities)

        self.assertEqual(100, civ.gold)
        with self.assertRaises(ValueError):
            civ.gold = "gold"
        self.assertEqual(100, civ.gold)
