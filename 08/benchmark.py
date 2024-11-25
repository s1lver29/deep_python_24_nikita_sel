# pylint: disable=R0903, W0621

import timeit
import weakref
import gc
from memory_profiler import profile

N = 10**7


class RegularClass:
    def __init__(self, a):
        self.a = a
        self.letter = chr((self.a % 26) + 65)


class SlotsClass:
    __slots__ = ("a", "letter", "hex")

    def __init__(self, a):
        self.a = a
        self.letter = chr((self.a % 26) + 65)


class WeakRefClass:
    __slots__ = ("__weakref__", "a", "letter", "hex")

    def __init__(self, a):
        self.a = a
        self.letter = chr((a % 26) + 65)


@profile
def create_regular(N=10**5):
    instances = [RegularClass(i) for i in range(N)]
    return instances


@profile
def create_slots(N=10**5):
    instances = [SlotsClass(i) for i in range(N)]
    return instances


@profile
def create_weakref(N=10**5):
    instances = [WeakRefClass(i) for i in range(N)]
    instances_weakref = [weakref.ref(item) for item in instances]
    return instances, instances_weakref


@profile
def read_modify(instances):
    for obj in instances:
        obj.a += 1
        obj.letter = chr((obj.a % 26) + 65)


@profile
def read_modify_weakref(instances_weakref):
    for weak_obj in instances_weakref:
        obj = weak_obj()
        if obj is not None:
            obj.a += 1
            obj.letter = chr((obj.a % 26) + 65)


if __name__ == "__main__":
    time_regular_create = timeit.timeit(lambda: create_regular(N), number=1)
    time_slots_create = timeit.timeit(lambda: create_slots(N), number=1)
    time_weakref_create = timeit.timeit(lambda: create_weakref(N), number=1)

    # Измерение времени чтения и изменения атрибутов
    instances_regular = create_regular(N)
    time_regular_modify = timeit.timeit(
        lambda: read_modify(instances_regular), number=1
    )
    del instances_regular
    gc.collect()

    instances_slots = create_slots(N)
    time_slots_modify = timeit.timeit(
        lambda: read_modify(instances_slots), number=1
    )
    del instances_slots
    gc.collect()

    instances, instances_weakref = create_weakref(N)
    time_weakref_modify = timeit.timeit(
        lambda: read_modify_weakref(instances_weakref), number=1
    )
    del instances
    gc.collect()

    print("Creation Times:")
    print(f"  Regular: {time_regular_create:.3f}s")
    print(f"  Slots: {time_slots_create:.3f}s")
    print(f"  WeakRef: {time_weakref_create:.3f}s")
    print("\nAccess Times (Modify):")
    print(f"  Regular: {time_regular_modify:.3f}s")
    print(f"  Slots: {time_slots_modify:.3f}s")
    print(f"  WeakRef: {time_weakref_modify:.3f}s")
