from typing import Type, Any, List
from functools import wraps


def retry_deco(
    retries: int | None = None, exceptions: List[Type[Exception]] | None = None
):
    if exceptions is None:
        exceptions = []
    if retries is None:
        retries = 1

    if isinstance(exceptions, list) and all(
        isinstance(exception, type) for exception in exceptions
    ):
        print("ok")

    def decorator(func) -> Any:
        @wraps(func)
        def wrappers(*args, **kwargs) -> Any:
            info_function = (
                f'run "{func.__name__}" with ',
                f"positional {args=}, " if args else "",
                f"keyword {kwargs=}, " if kwargs else "",
            )
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    print(*info_function, f"{attempt=}, {result=}", sep="")
                    return result
                except Exception as error:  # pylint: disable=broad-except
                    print(
                        *info_function,
                        f"attempt = {attempt + 1}, "
                        f"exception = {error.__class__.__name__}",
                        sep="",
                    )
                    if (
                        isinstance(error, tuple(exceptions))
                        or attempt + 1 == retries
                    ):
                        raise error
            return None

        return wrappers

    return decorator
