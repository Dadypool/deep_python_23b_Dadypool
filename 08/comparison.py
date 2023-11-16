"Homework 8. Comparing dict, slots and weakref"

import weakref
import time
# import cProfile
# import pstats
# from memory_profiler import profile


class MyObject:
    "Other classes will be using it"

    def __init__(self):
        self.val = 1


class MyClass:
    "Class with standard attributes"

    def __init__(self):
        self.first = MyObject()
        self.second = MyObject()
        self.third = MyObject()


class MySlots:
    "Class with slots"

    __slots__ = ("first", "second", "third")

    def __init__(self):
        self.first = MyObject()
        self.second = MyObject()
        self.third = MyObject()


class MyWeakRef:
    "Class with weakrefs"

    def __init__(self):
        self._first_init = MyObject()
        self._second_init = MyObject()
        self._third_init = MyObject()

        self.first = weakref.ref(self._first_init)
        self.second = weakref.ref(self._second_init)
        self.third = weakref.ref(self._third_init)


def compare_time(n, deg):
    "Time comparison"
    N_times = 2

    times = [0] * 6
    for _ in range(N_times):
        t_myclasses_init, t_myclass_rw = run_myclasses(n)
        times[0] += t_myclasses_init
        times[1] += t_myclass_rw
        t_myslots_init, t_myslots_rw = run_myslots(n)
        times[2] += t_myslots_init
        times[3] += t_myslots_rw
        t_myweakrefs_init, t_myweakrefs_rw = run_myweakrefs(n)
        times[4] += t_myweakrefs_init
        times[5] += t_myweakrefs_rw

    print("=" * 40)
    print(f"Compare time init for 10**{deg} objects: ")
    print(f"\tMyClass with __dict__: {times[0] / N_times:.2f} seconds")
    print(f"\tMyClass with __slots__: {times[2] / N_times:.2f} seconds")
    print(f"\tMyClass with weakref: {times[4] / N_times:.2f} seconds")

    print("=" * 40)
    print(f"Compare time red/write for 10**{DEG} objects: ")
    print(f"\tMyClass with __dict__: {times[1] / N_times:.2f} seconds")
    print(f"\tMyClass with __slots__: {times[3] / N_times:.2f} seconds")
    print(f"\tMyClass with weakref time red/write: {times[5] / N_times:.2f} seconds")
    print("=" * 40)


# @profile
def run_myclasses(n):
    "Run MyClass"

    t_init_start = time.perf_counter()
    my_classes = [MyClass() for _ in range(n)]
    t_init_end = time.perf_counter()

    t_rw_start = time.perf_counter()
    for myclass in my_classes:
        myclass.first.val = 100
        myclass.second.val += 100
        myclass.third.val *= 100
    t_rw_end = time.perf_counter()

    return t_init_end - t_init_start, t_rw_end - t_rw_start


# @profile
def run_myslots(n):
    "Run MySlots"

    t_init_start = time.perf_counter()
    my_slots = [MySlots() for _ in range(n)]
    t_init_end = time.perf_counter()

    t_rw_start = time.perf_counter()
    for myslot in my_slots:
        myslot.first.val = 100
        myslot.second.val += 100
        myslot.third.val *= 100
    t_rw_end = time.perf_counter()

    return t_init_end - t_init_start, t_rw_end - t_rw_start


# @profile
def run_myweakrefs(n):
    "Run MyWeakRef"

    t_init_start = time.perf_counter()
    my_wekrefs = [MyWeakRef() for _ in range(n)]
    t_init_end = time.perf_counter()

    t_rw_start = time.perf_counter()
    for myweakref in my_wekrefs:
        myweakref.first().val = 100
        myweakref.second().val += 100
        myweakref.third().val *= 100
    t_rw_end = time.perf_counter()

    return t_init_end - t_init_start, t_rw_end - t_rw_start


if __name__ == "__main__":
    DEG = 6
    N = 10**DEG

    # compare_time(N, DEG)

    # pr = cProfile.Profile()
    # pr.enable()
    run_myclasses(N)
    run_myslots(N)
    run_myweakrefs(N)
    # pr.disable()
    # stats = pstats.Stats(pr)
    # stats.sort_stats("ncalls").print_stats()
