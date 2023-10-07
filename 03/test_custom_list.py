"Homework 3 with tests for CustomList class"

from unittest import TestCase

from custom_list import CustomList


class TestDecor(TestCase):
    "Class with tests"

    def setUp(self):
        self.cust_list1 = CustomList([5, 1, 3, 7])

    def test_base_work(self):
        "Test indexing and append, extend, pop, insert, del, remove, len funcs"

        self.cust_list1.pop(1)
        self.assertEqual(self.cust_list1, CustomList([5, 3, 7]))
        self.assertEqual(3, len(self.cust_list1))

        self.cust_list1.append(0)
        self.assertEqual(self.cust_list1, CustomList([5, 3, 7, 0]))

        del self.cust_list1[2]
        self.assertEqual(self.cust_list1, CustomList([5, 3, 0]))

        self.cust_list1.insert(2, 10)
        self.assertEqual(self.cust_list1, CustomList([5, 3, 10, 0]))

        self.cust_list1.remove(3)
        self.assertEqual(self.cust_list1, CustomList([5, 10, 0]))

        self.cust_list1.extend([3, 4])
        self.assertEqual(self.cust_list1, CustomList([5, 10, 0, 3, 4]))

    def test_add(self):
        "Test add"

        # Same size
        cust_list2 = CustomList([1, 1, 1, 1])
        self.assertEqual(self.cust_list1 + cust_list2, CustomList([6, 2, 4, 8]))

        # Diff size
        cust_list2 = CustomList([1, 1])
        self.assertEqual(self.cust_list1 + cust_list2, CustomList([6, 2, 3, 7]))

        # With list
        lst = [1, 1]
        self.assertEqual(self.cust_list1 + lst, CustomList([6, 2, 3, 7]))
        self.assertEqual(lst + self.cust_list1, CustomList([6, 2, 3, 7]))

    def test_sub(self):
        "Test sub"

        # Same size
        cust_list2 = CustomList([1, 1, 1, 1])
        self.assertEqual(self.cust_list1 - cust_list2, CustomList([4, 0, 2, 6]))

        # Diff size
        cust_list2 = CustomList([1, 1])
        self.assertEqual(self.cust_list1 - cust_list2, CustomList([4, 0, 3, 7]))

        # With list
        lst = [1, 1]
        self.assertEqual(self.cust_list1 - lst, CustomList([4, 0, 3, 7]))
        self.assertEqual(lst - self.cust_list1, CustomList([-4, 0, -3, -7]))

    def test_compare(self):
        "Test comparison"

        cust_list2 = CustomList([7, 3, 1, 5])
        self.assertTrue(self.cust_list1 == cust_list2)
        self.assertTrue(self.cust_list1 >= cust_list2)
        self.assertTrue(self.cust_list1 <= cust_list2)
        self.assertFalse(self.cust_list1 > cust_list2)

        cust_list2.append(1)
        self.assertTrue(self.cust_list1 < cust_list2)
        self.assertTrue(self.cust_list1 <= cust_list2)
        self.assertTrue(self.cust_list1 != cust_list2)
        self.assertFalse(self.cust_list1 > cust_list2)
        self.assertFalse(self.cust_list1 == cust_list2)

    def test_str(self):
        "Test str"

        self.assertEqual(str(self.cust_list1), "[5, 1, 3, 7]  Sum: 16")

    def test_repr(self):
        "Test repr"

        self.assertEqual(repr(self.cust_list1), "CustomList([5, 1, 3, 7])")

    def test_non_numeric_types(self):
        "Test create CustomList with non numeric list"

        with self.assertRaises(TypeError):
            CustomList(["E", "n", "d"])

        with self.assertRaises(TypeError):
            self.cust_list1.append([1, 2, 3])

        with self.assertRaises(TypeError):
            self.cust_list1.extend([1, "2", 3])

        with self.assertRaises(TypeError):
            self.cust_list1.insert(2, "2")

    def test_empty_list(self):
        "Test creating CustomList with empty list"

        empty_cust_list = CustomList()
        self.assertEqual(0, len(empty_cust_list))
        self.assertFalse(empty_cust_list)

    def test_float(self):
        "Test CustomList with floats"

        cust_list2 = CustomList([5, 1, 3, 7.0])
        self.assertTrue(self.cust_list1 == cust_list2)
        cust_list2[-1] += 0.1
        self.assertFalse(self.cust_list1 == cust_list2)
        cust_list2[-1] -= 0.100000001
        self.assertTrue(self.cust_list1 == cust_list2)
