from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: str | int | tuple
    value: Any
    prev: "Node" = None
    next: "Node" = None


class LRUCache:
    """Класс для реализации LRU-кэша."""

    def __init__(self, limit: int = 42):
        if not isinstance(limit, int) or limit <= 0:
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

    def _remove(self, node: "Node") -> None:
        """Удаление узла из двусвязного списка."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: "Node") -> None:
        """Добавление узла в начало двусвязного списка (после головы)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _rotate(self, node: "Node") -> None:
        self._remove(node)
        self._add(node)

    def get(self, key: str | int | tuple):
        """Получение значения по ключу."""
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._rotate(node)
        return node.value

    def set(self, key: str | int | tuple, value: Any):
        """Установка значения по ключу."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._rotate(node)
        else:
            if len(self.cache) == self.limit:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)

    def __getitem__(self, key):
        """Аналог метода get для обращения через []."""
        return self.get(key)

    def __setitem__(self, key: str | int | tuple, value: Any):
        """Аналог метода set для присваивания через []."""
        self.set(key, value)
