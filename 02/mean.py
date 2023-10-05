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
            n_calls = k if len(last_calls) == k else len(last_calls)
            print(
                f"Mean time of last {n_calls} calls: {round(sum(last_calls) / k, 2)}s"
            )
            return res

        return wrapper

    return decorator
