from typing import Type, Any, List
from functools import wraps


def retry_deco(
    retries: int | None = None, exceptions: List[Type[Exception]] | None = None
):
    if exceptions is None:
        exceptions = []
    if retries is None:
        retries = 1

    if not isinstance(retries, int) or isinstance(retries, bool):
        raise TypeError(
            "retries должен быть числом (int) или быть пустым"
        )
    if retries < 1:
        raise ValueError(
            "retries должно быть больше нуля (> 0)"
        )

    if not isinstance(exceptions, list) or not all(
        issubclass(exception, Exception) for exception in exceptions
    ):
        raise TypeError(
            "exception должен быть списком с объектами ислючениями "
            "или быть пустым"
        )

    def decorator(func) -> Any:
        @wraps(func)
        def wrappers(*args, **kwargs) -> Any:  # pylint: disable = R1710
            info_function = (
                f'run "{func.__name__}" with ',
                f"positional {args=}, " if args else "",
                f"keyword {kwargs=}, " if kwargs else "",
            )
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    print(*info_function,
                          f"attempt = {attempt + 1}, {result=}",
                          sep="")
                    return result
                except Exception as error:  # pylint: disable=broad-except
                    print(
                        *info_function,
                        f"attempt = {attempt + 1}, "
                        f"exception = {error.__class__.__name__}, "
                        f"info_exception = {error}",
                        sep="",
                    )
                    if (
                        isinstance(error, tuple(exceptions))
                        or attempt + 1 == retries
                    ):
                        raise error

        return wrappers

    return decorator


# @retry_deco(None, None)
# def add(a, b):
#     return a + b


# if __name__ == "__main__":
#     add(a=None, b=2)
