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
    count_collection = 10000
    number_iteration = 1000

    print(f"Generating large JSON data... size={count_collection}")
    large_json = generate_collection_large_json(count=10000)
    parsed_data = [json.loads(item) for item in large_json]

    print("\nMeasuring performance using timeit...")
    json_parsing_time = timeit.timeit(
        lambda: test_parsing(large_json, "json"), number=1000
    )

    custom_parsing_time = timeit.timeit(
        lambda: test_parsing(large_json, "custom_json"), number=1000
    )

    json_serialization_time = timeit.timeit(
        lambda: test_serialization(parsed_data, "custom_json"), number=1000
    )

    custom_serialization_time = timeit.timeit(
        lambda: test_serialization(parsed_data, "custom_json"), number=1000
    )

    print(f"\nPerformance Results ({number_iteration} iterations):")
    print(
        f"Standard JSON - Parsing: {json_parsing_time:.3f}s, "
        f"Serialization: {json_serialization_time:.3f}s"
    )
    print(
        f"Custom JSON   - Parsing: {custom_parsing_time:.3f}s, "
        f"Serialization: {custom_serialization_time:.3f}s"
    )


if __name__ == "__main__":
    main()
