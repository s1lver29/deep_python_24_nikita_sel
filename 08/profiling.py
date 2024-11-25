import cProfile
import pstats
from io import StringIO
from .benchmark import (
    N,
    create_regular,
    create_slots,
    create_weakref,
    read_modify,
    read_modify_weakref,
)


def profile_cpu(func, name):
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    print(f"\nCPU Profile for {name}:\n")
    stats.print_stats()
    return stream.getvalue()


if __name__ == "__main__":
    # Профилирование RegularClass
    print("Profiling RegularClass:")
    print(profile_cpu(lambda: create_regular(N), "Create RegularClass"))
    instances_regular = create_regular(N)
    print(
        profile_cpu(
            lambda: read_modify(instances_regular), "Read/Modify RegularClass"
        )
    )

    # Профилирование SlotsClass
    print("\nProfiling SlotsClass:")
    print(profile_cpu(lambda: create_slots(N), "Create SlotsClass"))
    instances_slots = create_slots(N)
    print(
        profile_cpu(
            lambda: read_modify(instances_slots), "Read/Modify SlotsClass"
        )
    )

    # Профилирование WeakRefClass
    print("\nProfiling WeakRefClass:")
    print(profile_cpu(lambda: create_weakref(N), "Create WeakRefClass"))
    instances, instances_weakref = create_weakref(N)
    print(
        profile_cpu(
            lambda: read_modify_weakref(instances_weakref),
            "Read/Modify WeakRefClass",
        )
    )
