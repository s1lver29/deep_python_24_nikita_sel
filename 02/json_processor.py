import json
from typing import Callable


def _process_words(
    key: str, words: list[str], callback: Callable[[str, str], None] | None
):
    """Обработка слов без токенов"""
    for word in words:
        callback(key, word)


def _process_tokens(
    key: str,
    lower_words: list[str],
    lower_tokens: list[str],
    tokens: list[str],
    callback: Callable[[str, str], None] | None = None,
):
    """Обработка слов с токенами"""
    for token in lower_words:
        if token in lower_tokens:
            callback(key, tokens[lower_tokens.index(token)])


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    try:
        data = json.loads(json_str)
    except Exception as error:
        raise error

    required_keys = required_keys if required_keys is not None else []
    tokens = tokens if tokens is not None else []

    if not isinstance(required_keys, list) or not all(
        isinstance(item, str) for item in required_keys
    ):
        raise TypeError(
            "required_keys должен быть списком со строковыми объектами "
            "или быть пустым"
        )

    if not isinstance(tokens, list) or not all(
        isinstance(item, str) for item in tokens
    ):
        raise TypeError(
            "tokens должен быть списком со строковыми объектами "
            "или быть пустым"
        )

    if not callable(callback) and callback is not None:
        raise TypeError(
            "callback является Callable[[str, str], None] или быть None"
        )

    lower_tokens = [token.lower() for token in tokens] if tokens else []

    for key, value in data.items():
        words = value.split()
        if callback is None:
            break

        if not required_keys or key in required_keys:
            lower_words = [word.lower() for word in words]

            if not tokens:
                _process_words(key, words, callback)
            else:
                _process_tokens(
                    key, lower_words, lower_tokens, tokens, callback
                )
