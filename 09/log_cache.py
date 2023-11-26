"Homework 9. Logging lru_cache"

import logging

logger = logging.getLogger("__name__")


class Node:
    "class for Nodes containing key and value"

    def __init__(self, key=None, val=None):
        logger.debug("Node.__init__")
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCache:
    "Last Recently Used Cache"

    def __init__(self, limit=42):
        logger.debug("LRUCache.__init__")
        self.hash = {}
        self.limit = limit
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        "Gets value from key else None"

        logger.debug("LRUCache.get(%d)", key)
        if key not in self.hash:
            logger.info("Key %d not found in cache", key)
            return None

        node = self.hash[key]
        self._move(node)

        logger.info("Key %d found in cache", key)
        return node.val

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, value):
        "Puts item in cache. If capacity is limit, delete the most unused item"

        logger.debug("LRUCache.set(%d, %d)", key, value)
        if key not in self.hash:
            if len(self.hash) == self.limit:
                self.hash.pop(self.tail.prev.key)
                self._remove(self.tail.prev)
                logger.info("Cache is full. Deleting %d", self.tail.prev.key)

            node = Node(key, value)
            self.hash[key] = node
            self._add(node)
            logger.info("Key %d added to cache", key)
        else:
            node = self.hash[key]
            node.val = value

            if self.head.next != node:
                self._move(node)
            logger.info("Key %d updated in cache", key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def _move(self, node):
        "Moves node to the top of the list"

        logger.debug("LRUCache._move(%d)", node.key)

        self._remove(node)

        node.next = self.head.next
        node.next.prev = node

        node.prev = self.head
        self.head.next = node

    def _add(self, node):
        "Adds node to the top of the list"

        logger.debug("LRUCache._add(%d)", node.key)
        node.prev = self.head
        node.next = self.head.next

        self.head.next = node
        node.next.prev = node

    def _remove(self, node):
        "Removes node from the list"

        logger.debug("LRUCache._remove(%d)", node.key)
        node.prev.next = node.next
        node.prev.next = node.next
        node.next.prev = node.prev


def logger_config(stdout, log_filter, debug):
    "Configures logger"

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("cache.log", mode="w")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if stdout:
        stdout_handler = logging.StreamHandler()
        stdout_formatter = logging.Formatter(
            "%(filename)s:%(lineno)s - %(levelname)s - %(message)s"
        )
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)
    if log_filter:
        logger.addFilter(MyFilter())
    if debug:
        logger.setLevel(logging.DEBUG)


class MyFilter(logging.Filter):
    "Custom filter for logging"

    def filter(self, record):
        return record.lineno % 2


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Master-Worker Server")
    parser.add_argument(
        "-s", "--stdout", action="store_true", help="Additional logging to stdout"
    )
    parser.add_argument(
        "-f", "--filter", action="store_true", help="Enable custom filter"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Disable debug logs")
    args = parser.parse_args()

    # Config logger
    logger_config(args.stdout, args.filter, args.debug)

    # Lru_cache work
    cache = LRUCache(3)
    cache[1] = 1
    cache[2] = 20
    cache[3] = 30
    cache[1] = 10

    assert cache[1] == 10

    cache[4] = 40

    assert cache[5] is None
