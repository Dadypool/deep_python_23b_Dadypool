"Homework 2 with decorator of mean time of k last calls"

from time import time, sleep
from random import random
from collections import deque


def mean(k, last_calls=deque([])):   # pylint: disable=(W0102, C0116)
    def decorator(func):
        def wrapper(*args, **kwargs):
            "Decorator count mean time of k last calls of func"

            start = time()
            func(*args, **kwargs)
            end = time()
            if len(last_calls) == k:
                last_calls.popleft()
            last_calls.append(end - start)
            n_calls = k if len(last_calls) == k else len(last_calls)
            print(f'Mean time of last {n_calls} calls: {round(sum(last_calls) / k, 2)}s')
        return wrapper
    return decorator


@mean(10)
def foo(arg1):
    print(f'foo: {arg1}')
    sleep(random()*0.5)


@mean(2)
def boo(arg1):
    print(f'boo: {arg1}')
    sleep(random()*0.75)


if __name__ == '__main__':
    for _ in range(100):
        foo("Walter")
