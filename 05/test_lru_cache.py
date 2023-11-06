"Homework 5 with tests for LRU Cache"

from unittest import TestCase

from lru_cache import LRUCache


class TestLRUCache(TestCase):
    "Class with tests"

    def count_nodes(self, head, tail):
        "Counts nodes in list for tests"

        n_nodes = 0
        node = head
        while node.next != tail:
            n_nodes += 1
            node = node.next

        return n_nodes

    def test_base_work(self):
        "Tests base work of LRU Cache with get set operations"

        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))

    def test_get_set_item(self):
        "Tests getitem and setitiem"

        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"

        self.assertIsNone(cache["k3"])
        self.assertEqual(cache["k2"], "val2")
        self.assertEqual(cache["k1"], "val1")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))

    def test_limit(self):
        "Tests work of capacity"

        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"
        cache["k3"] = "val3"

        self.assertIsNone(cache["k1"])
        self.assertEqual(cache["k3"], "val3")
        self.assertEqual(cache["k2"], "val2")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))

        cache["k1"] = "val1"
        self.assertIsNone(cache["k3"])
        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))

    def test_with_capacity_1(self):
        "Tests lru cache with capacity 1"

        cache = LRUCache(1)

        cache["k1"] = "val1"
        cache["k2"] = "val2"
        cache["k3"] = "val3"

        self.assertIsNone(cache["k1"])
        self.assertIsNone(cache["k2"])
        self.assertEqual(cache["k3"], "val3")

        self.assertEqual(1, len(cache.hash))
        self.assertEqual(1, self.count_nodes(cache.head, cache.tail))
        self.assertEqual(cache.head.next.key, "k3")

    def test_update_existing_key(self):
        "Tests work if update existing key. Non-updated keys come last"

        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"

        cache["k1"] = "val1_1"

        cache["k3"] = "val3"

        self.assertIsNone(cache["k2"])
        self.assertEqual(cache["k1"], "val1_1")
        self.assertEqual(cache["k3"], "val3")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))
        self.assertEqual(cache.head.next.key, "k3")
        self.assertEqual(cache.head.next.next.key, "k1")

    def test_update_one_item_several_times(self):
        "Tests work if udate one item several times"

        cache = LRUCache(2)

        cache["k1"] = "val1"
        cache["k2"] = "val2"

        cache["k1"] = "val1_1"
        cache["k1"] = "val1_2"

        self.assertEqual(cache["k1"], "val1_2")
        cache["k1"] = "val1_3"
        self.assertEqual(cache["k1"], "val1_3")

        self.assertEqual(2, len(cache.hash))
        self.assertEqual(2, self.count_nodes(cache.head, cache.tail))
        self.assertEqual(cache.head.next.key, "k1")
        self.assertEqual(cache.head.next.next.key, "k2")
