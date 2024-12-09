# pylint: disable=I1101

import json
import random
import timeit

from faker import Faker

import custom_json


def generate_collection_large_json(count=1000):
    """Генерирует большой JSON-массив с использованием Faker."""
    fake = Faker()
    data = []
    for _ in range(count):
        obj = {
            "name": fake.name(),
            "address": " ".join(fake.address().split()),
            "email": fake.email(),
            "age": random.randint(18, 99),
            "salary": random.randint(30000, 150000),
            "projects": fake.bs(),
            "string_data": fake.text(max_nb_chars=200),
            "number_data": fake.random_number(),
        }
        data.append(json.dumps(obj))
    return data


def test_parsing(data, library):
    """Тестирует парсинг JSON-строки."""
    if library == "json":
        return [json.loads(item) for item in data]
    if library == "custom_json":
        return [custom_json.loads(item) for item in data]
    raise ValueError("Unknown library")


def test_serialization(obj, library):
    """Тестирует сериализацию объекта в JSON-строку."""
    if library == "json":
        return [json.dumps(item) for item in obj]
    if library == "custom_json":
        return [custom_json.dumps(item) for item in obj]
    raise ValueError("Unknown library")


def main():
    count_collection = 10_000
    number_iteration = 1_000
    time_benchmark = {}

    print(f"Generating large JSON data... size={count_collection}")
    large_json = generate_collection_large_json(count=count_collection)
    parsed_data = [json.loads(item) for item in large_json]

    print("\nMeasuring performance using timeit...")
    function_test = [test_parsing, test_serialization]
    data_test = [large_json, parsed_data]

    for func, data in zip(function_test, data_test):
        for library in ("json", "custom_json"):
            print(f"Start benchmark {library} - {func.__name__}")
            time_benchmark[(func.__name__, library)] = timeit.timeit(
                lambda f=func, data=data, lib=library: f(data, lib),
                number=number_iteration,
            )

    print(f"\nPerformance Results ({number_iteration} iterations):")
    print(
        "Standard JSON - Parsing: "
        f"{time_benchmark[("test_parsing", "json")]:.3f}s, "
        "Serialization: "
        f"{time_benchmark[("test_serialization", "json")]:.3f}s"
    )
    print(
        "Custom JSON   - Parsing: "
        f"{time_benchmark[("test_parsing", "custom_json")]:.3f}s, "
        "Serialization: "
        f"{time_benchmark[("test_serialization", "custom_json")]:.3f}s"
    )


if __name__ == "__main__":
    main()
