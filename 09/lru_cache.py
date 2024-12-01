import argparse
import logging
import logging.config
from dataclasses import dataclass
from typing import Any

import yaml


# pylint: disable=too-few-public-methods
class ExcludeMagicAndNonPublicMethodsFilter(logging.Filter):
    """
    Фильтрация логирования:
        Фильтруются non-public и magic методы класса.
        Не производится их логирование
    """
    def filter(self, record):
        if record.funcName.startswith("__") or record.funcName.startswith("_"):
            return False
        return True


def configure_logging(to_stdout=False, apply_filter=False):
    with open("logging_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if to_stdout:
        console_handler = {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "formatter_stdout",
            "stream": "ext://sys.stdout",
        }
        config["handlers"]["console"] = console_handler
        config["loggers"]["lru_cache_logger"]["handlers"].append("console")

    if apply_filter:
        exclude_magic_nonpublic_filter = {
            "()": ExcludeMagicAndNonPublicMethodsFilter
        }
        config["filters"] = {
            "exclude_magic_nonpublic_filter": exclude_magic_nonpublic_filter
        }

        for handler in config["handlers"].values():
            if "filters" not in handler:
                handler["filters"] = ["exclude_magic_nonpublic_filter"]

    logging.config.dictConfig(config)


@dataclass
class Node:
    key: str | int | tuple
    value: Any
    prev: "Node" = None
    next: "Node" = None


class LRUCache:
    """Класс для реализации LRU-кэша."""

    def __init__(self, limit: int = 42):
        self.logger = logging.getLogger("lru_cache_logger")
        if not isinstance(limit, int) or limit <= 0:
            self.logger.error("Invalid limit: limit=%d", limit)
            raise ValueError(
                f"Получено {limit=}, <{type(limit).__name__}>. "
                "limit должен быть > 0 и целочисленным"
            )
        self.limit = limit
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.logger.debug("Cache created with limit: %d", limit)

    def _remove(self, node: "Node") -> None:
        """Удаление узла из двусвязного списка."""
        self.logger.debug(
            "Removing node: key=%s, value=%s", node.key, node.value
        )

        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: "Node") -> None:
        """Добавление узла в начало двусвязного списка (после головы)."""
        self.logger.debug(
            "Adding node: key=%s, value=%s", node.key, node.value
        )

        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _rotate(self, node: "Node") -> None:
        self.logger.debug(
            "Moving node to front: key=%s, value=%s", node.key, node.value
        )

        self._remove(node)
        self._add(node)

    def get(self, key: str | int | tuple):
        """Получение значения по ключу."""
        self.logger.debug("Attempting to get value for key: %s", key)
        if key not in self.cache:
            self.logger.info("GET key=%s: NO VALUE", key)
            return None
        node = self.cache[key]
        self._rotate(node)

        self.logger.info("GET key=%s: value=%s", key, node.value)
        self.logger.debug("Cache state after GET: %s", list(self.cache.keys()))

        return node.value

    def set(self, key: str | int | tuple, value: Any):
        """Установка значения по ключу."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._rotate(node)
            self.logger.info("SET key=%s: UPDATED value=%s", key, value)
        else:
            if len(self.cache) == self.limit:
                lru_node = self.tail.prev
                self.logger.debug(
                    "Cache is full. Removing LRU key=%s, value=%s",
                    lru_node.key,
                    lru_node.value,
                )
                self._remove(lru_node)
                del self.cache[lru_node.key]
                self.logger.info(
                    "SET key=%s: EVICTION lru_node.key=%s, lru_node.value=%s",
                    key,
                    lru_node.key,
                    lru_node.value,
                )
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)

            self.logger.info("SET key=%s: INSERTED value=%s", key, value)
            self.logger.debug(
                "Cache state after SET: %s", list(self.cache.keys())
            )

    def __getitem__(self, key):
        """Аналог метода get для обращения через []."""
        self.logger.debug("__getitem__ called for key: %s", key)
        value = self.get(key)
        if value is None:
            self.logger.debug("__getitem__: Key %s not found.", key)
        else:
            self.logger.debug(
                "__getitem__: Retrieved value %s for key %s.", value, key
            )
        return value

    def __setitem__(self, key: str | int | tuple, value: Any):
        """Аналог метода set для присваивания через []."""
        self.logger.debug(
            "__setitem__ called for key: %s, value: %s", key, value
        )
        self.set(key, value)
        self.logger.debug("__setitem__: Key %s set with value %s.", key, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LRUCache with logging. Logging goes to the cache.log file"
    )
    parser.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="Enable logging to stdout",
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="store_true",
        help="Apply logging filter. "
        "Non-public and magic methods of the class will not be logged",
    )
    args = parser.parse_args()

    configure_logging(to_stdout=args.stdout, apply_filter=args.filter)

    try:
        LRUCache(-1)
    except ValueError:
        pass

    cache = LRUCache(3)

    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.get("k1")
    cache.get("k3")
    cache.set("k3", "v3")
    cache.set("k4", "v4")
    cache.set("k1", "new_v1")

    cache["k3"] = "new_v3"
    temp = cache["k4"]
