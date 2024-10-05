import json
from typing import Callable


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
            "callback является Callable[[str, str], None] " "или быть None"
        )

    if tokens:
        lower_tokens = [token.lower() for token in tokens]

    for key, value in data.items():
        words = value.split()
        if callback is None:
            break

        if not required_keys or key in required_keys:
            lower_words = [word.lower() for word in words]

            if not tokens:
                for word in words:
                    callback(key, word)
            else:
                for token in lower_words:
                    if token in lower_tokens:
                        callback(key, tokens[lower_tokens.index(token)])


if __name__ == "__main__":
    json_str = '{"key1": "Word1 word2 WoRd1", "key2": "word2 word3"}'
    required_keys = ["key1", "KEY2"]
    tokens = ["WORD1", "word2"]

    process_json(
        json_str,
        required_keys=required_keys,
        tokens=tokens,
        # callback=None
        callback=lambda key, token: print(f"{key=}, {token=}"),
    )
