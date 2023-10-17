"Homework 5 with LRU Cache"


class Node:
    "class for Nodes containing key and value"

    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    "Last Recently Used Cache"

    def __init__(self, limit=42):
        self.hash = {}
        self.limit = limit
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        "Gets value from key else None"

        if key not in self.hash:
            return None

        node = self.hash[key]
        self._move(node)

        return node.val

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, value):
        "Puts item in cache. If capacity is limit, delete the most unused item"

        if key not in self.hash:
            if len(self.hash) == self.limit:
                self.hash.pop(self.tail.prev.key)
                self._remove(self.tail.prev)

            node = Node(key, value)
            self.hash[key] = node
            self._add(node)
        else:
            node = self.hash[key]
            node.val = value

            if self.head.next != node:
                self._move(node)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def _move(self, node):
        "Moves node to the top of the list"

        self._remove(node)

        node.next = self.head.next
        node.next.prev = node

        node.prev = self.head
        self.head.next = node

    def _add(self, node):
        "Adds node to the top of the list"

        node.prev = self.head
        node.next = self.head.next

        self.head.next = node
        node.next.prev = node

    def _remove(self, node):
        "Removes node from the list"

        node.prev.next = node.next
        node.next.prev = node.prev
