"Homework 2 with decorator of mean time of k last function calls"

from time import time
from functools import wraps
from collections import deque


def mean(k: int = 10):
    "Decorator counts mean time of k last calls of func"

    last_calls = deque([], k)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            "Wrapper func"

            start = time()
            res = func(*args, **kwargs)
            end = time()

            last_calls.append(end - start)
            print(
                f"Mean time of last {len(last_calls)} calls: {round(sum(last_calls) / len(last_calls), 2)}s"
            )
            return res

        return wrapper

    return decorator
