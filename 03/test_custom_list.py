"Homework 3 with tests for CustomList class"

from unittest import TestCase

from custom_list import CustomList


class TestDecor(TestCase):
    "Class with tests"

    def test_base_work(self):
        "Test indexing and append, extend, pop, insert, del, remove, len funcs"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list1.pop(1)
        expect_list = CustomList([5, 3, 7])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

        cust_list1.append(0)
        expect_list = CustomList([5, 3, 7, 0])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

        del cust_list1[2]
        expect_list = CustomList([5, 3, 0])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

        cust_list1.insert(2, 10)
        expect_list = CustomList([5, 3, 10, 0])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

        cust_list1.remove(3)
        expect_list = CustomList([5, 10, 0])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

        cust_list1.extend([3, 4])
        expect_list = CustomList([5, 10, 0, 3, 4])
        self.assertEqual(len(expect_list), len(cust_list1))
        for i, j in zip(cust_list1, expect_list):
            self.assertEqual(i, j)

    def test_add_same_size(self):
        "Test add same size CustomLists"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([1, 1, 1, 1])
        res_list = cust_list1 + cust_list2
        exp_list = CustomList([6, 2, 4, 8])
        # Check resulted list
        self.assertEqual(len(res_list), len(exp_list))
        for i, j in zip(res_list, exp_list):
            self.assertEqual(i, j)
        # Check cust_list1 and cust_list2 didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(len(cust_list2), 4)
        for i, j in zip(cust_list2, CustomList([1, 1, 1, 1])):
            self.assertEqual(i, j)

    def test_add_diff_size(self):
        "Test add diff sizes CustomLists"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([1, 1])
        res_list1 = cust_list1 + cust_list2
        res_list2 = cust_list2 + cust_list1
        exp_list = CustomList([6, 2, 3, 7])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list))
        for i, j in zip(res_list1, exp_list):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list))
        for i, j in zip(res_list2, exp_list):
            self.assertEqual(i, j)
        # Check cust_list1 and cust_list2 didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
            self.assertEqual(len(cust_list2), 2)
        for i, j in zip(cust_list2, CustomList([1, 1])):
            self.assertEqual(i, j)

    def test_add_with_list_same_size(self):
        "Test add CustomList and list with same size"

        cust_list1 = CustomList([5, 1, 3, 7])
        lst = [1, 1, 1, 1]
        res_list = cust_list1 + lst
        exp_list = CustomList([6, 2, 4, 8])
        # Check resulted list
        self.assertEqual(len(res_list), len(exp_list))
        for i, j in zip(res_list, exp_list):
            self.assertEqual(i, j)
        # Check cust_list1 and lst didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(lst, [1, 1, 1, 1])

    def test_add_with_list_diff_size(self):
        "Test add CustomList and list with diff sizes"

        cust_list1 = CustomList([5, 1, 3, 7])
        lst = [1, 1]
        res_list1 = cust_list1 + lst
        res_list2 = lst + cust_list1
        exp_list = CustomList([6, 2, 3, 7])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list))
        for i, j in zip(res_list1, exp_list):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list))
        for i, j in zip(res_list2, exp_list):
            self.assertEqual(i, j)
        # Check cust_list1 and lst didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(lst, [1, 1])

    def test_sub_same_size(self):
        "Test sub same size CustomLists"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([1, 1, 1, 1])
        res_list1 = cust_list1 - cust_list2
        res_list2 = cust_list2 - cust_list1
        exp_list1 = CustomList([4, 0, 2, 6])
        exp_list2 = CustomList([-4, 0, -2, -6])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list1))
        for i, j in zip(res_list1, exp_list1):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list2))
        for i, j in zip(res_list2, exp_list2):
            self.assertEqual(i, j)
        # Check cust_list1 and cust_list2 didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(len(cust_list2), 4)
        for i, j in zip(cust_list2, CustomList([1, 1, 1, 1])):
            self.assertEqual(i, j)

    def test_sub_diff_size(self):
        "Test sub diff sizes CustomLists"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([1, 1])
        res_list1 = cust_list1 - cust_list2
        res_list2 = cust_list2 - cust_list1
        exp_list1 = CustomList([4, 0, 3, 7])
        exp_list2 = CustomList([-4, 0, -3, -7])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list1))
        for i, j in zip(res_list1, exp_list1):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list2))
        for i, j in zip(res_list2, exp_list2):
            self.assertEqual(i, j)
        # Check cust_list1 and cust_list2 didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(len(cust_list2), 2)
        for i, j in zip(cust_list2, CustomList([1, 1])):
            self.assertEqual(i, j)

    def test_sub_with_list_same_size(self):
        "Test sub CustomList and list with same size"

        cust_list1 = CustomList([5, 1, 3, 7])
        lst = [1, 1, 1, 1]
        res_list1 = cust_list1 - lst
        res_list2 = lst - cust_list1
        exp_list1 = CustomList([4, 0, 2, 6])
        exp_list2 = CustomList([-4, 0, -2, -6])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list1))
        for i, j in zip(res_list1, exp_list1):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list2))
        for i, j in zip(res_list2, exp_list2):
            self.assertEqual(i, j)
        # Check cust_list1 and lst didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(lst, [1, 1, 1, 1])

    def test_sub_with_list_diff_size(self):
        "Test sub CustomList and list with diff sizes"

        cust_list1 = CustomList([5, 1, 3, 7])
        lst = [1, 1]
        res_list1 = cust_list1 - lst
        res_list2 = lst - cust_list1
        exp_list1 = CustomList([4, 0, 3, 7])
        exp_list2 = CustomList([-4, 0, -3, -7])
        # Check resulted list
        self.assertEqual(len(res_list1), len(exp_list1))
        for i, j in zip(res_list1, exp_list1):
            self.assertEqual(i, j)
        self.assertEqual(len(res_list2), len(exp_list2))
        for i, j in zip(res_list2, exp_list2):
            self.assertEqual(i, j)
        # Check cust_list1 and lst didnt changed
        self.assertEqual(len(cust_list1), 4)
        for i, j in zip(cust_list1, CustomList([5, 1, 3, 7])):
            self.assertEqual(i, j)
        self.assertEqual(lst, [1, 1])

    def test_compare(self):
        "Test comparison"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([7, 3, 1, 5])
        self.assertTrue(cust_list1 == cust_list2)
        self.assertTrue(cust_list1 >= cust_list2)
        self.assertTrue(cust_list1 <= cust_list2)
        self.assertFalse(cust_list1 > cust_list2)

        cust_list2.append(1)
        self.assertTrue(cust_list1 < cust_list2)
        self.assertTrue(cust_list1 <= cust_list2)
        self.assertTrue(cust_list1 != cust_list2)
        self.assertFalse(cust_list1 > cust_list2)
        self.assertFalse(cust_list1 == cust_list2)

    def test_str(self):
        "Test str"

        self.assertEqual(str(CustomList([5, 1, 3, 7])), "[5, 1, 3, 7]  Sum: 16")

    def test_repr(self):
        "Test repr"

        self.assertEqual(repr(CustomList([5, 1, 3, 7])), "CustomList([5, 1, 3, 7])")

    def test_empty_list(self):
        "Test creating CustomList with empty list"

        empty_cust_list = CustomList()
        self.assertEqual(0, len(empty_cust_list))
        self.assertFalse(empty_cust_list)

    def test_float(self):
        "Test CustomList with floats"

        cust_list1 = CustomList([5, 1, 3, 7])
        cust_list2 = CustomList([5, 1, 3, 7.0])
        self.assertTrue(cust_list1 == cust_list2)
        cust_list2[-1] += 0.1
        self.assertFalse(cust_list1 == cust_list2)
        cust_list2[-1] -= 0.100000001
        self.assertTrue(cust_list1 == cust_list2)
