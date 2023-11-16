"Homework 8. Profile decorator"

import cProfile
import pstats
import functools


def profile_deco(func):
    "Profile decorator"

    func.profile = cProfile.Profile()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func.profile.enable()
            result = func(*args, **kwargs)
        finally:
            func.profile.disable()
        return result

    @functools.wraps(func)
    def print_stat():
        print("=" * 50)
        print(f"Profile stats for {func.__module__}.{func.__name__}:")
        stats = pstats.Stats(func.profile)
        stats.sort_stats("cumulative").print_stats()
        print("=" * 50)

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    "Function add"
    return a + b


@profile_deco
def sub(a, b):
    "Function sub"
    return a - b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
