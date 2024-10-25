from typing import Generator
from io import TextIOWrapper


def _should_yield(line: str, search_words: set, stop_words: set) -> bool:
    """
    Проверяет, следует ли возвращать строку
    на основе слов поиска и стоп-слов.
    """
    words = set(line.strip().lower().split())
    return bool(words & search_words) and not bool(words & stop_words)


def line_filter(
    file_filter: str | TextIOWrapper,
    search_words: list[str],
    stop_words: list[str] | None = None,
) -> Generator[str, None, None]:
    """
    Генератор, который читает строки из файла и фильтрует
    их по заданным критериям.

    Функция возвращает строки, содержащие хотя бы одно из слов для поиска,
    исключая те строки, которые содержат слова из списка стоп-слов.
    Поиск слов осуществляется по полному совпадению без учета регистра.

    Параметры:
    ----------
    file : Union[str, io.TextIOBase]
        Имя файла или объект файла, из которого будет производиться
        чтение строк.
    search_words : List[str]
        Список слов для поиска, строки из файла будут возвращены,
        если содержат хотя бы одно из этих слов.
    stop_words : List[str], optional
        Список стоп-слов. Если строка содержит хотя бы одно из этих слов,
        она будет проигнорирована. По умолчанию None, что означает отсутствие
        стоп-слов.

    Возвращает:
    ----------
    Generator[str, None, None]
        Генератор строк, соответствующих критериям фильтрации.

    Исключения:
    -----------
    TypeError
        Если аргументы не соответствуют ожидаемым типам.
    """
    stop_words = stop_words if stop_words is not None else []

    if not isinstance(file_filter, (str, TextIOWrapper)):
        raise TypeError(
            f"Получено {type(file_filter).__name__}, "
            "file должен быть str или тестовым объектом (TextIOWrapper)"
        )

    if not isinstance(search_words, list) or not all(
        isinstance(word, str) for word in search_words
    ):
        raise TypeError(
            "search_words должен быть списком со строковыми объектами"
        )

    if not isinstance(stop_words, list) or not all(
        isinstance(word, str) for word in stop_words
    ):
        raise TypeError(
            "stop_words должен быть списком со строковыми объектами "
            "или быть None"
        )

    search_words = set(word.lower() for word in search_words)
    stop_words = (
        set(word.lower() for word in stop_words) if stop_words else set()
    )

    with (
        open(file_filter, "r", encoding="utf-8")
        if isinstance(file_filter, str)
        else file_filter
    ) as f:
        for line in f:
            if _should_yield(line, search_words, stop_words):
                yield line.strip()
