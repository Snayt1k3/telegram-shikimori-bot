import asyncio
from logging import getLogger
from typing import Any, TypeVar, Awaitable, Callable

logger = getLogger("retry.logger")
FuncType = TypeVar("FuncType", bound=Callable[..., Awaitable[Any]])


def retry(
    *args: Any, num_attempts: int = 5, exp_size: int = 10
) -> FuncType | Callable[[FuncType], FuncType]:
    def decorator(func: FuncType) -> FuncType:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            exp = exp_size
            for _ in range(num_attempts):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.info(
                        f"Retry, func - {func.__module__}.{func.__name__}, error: {e}"
                    )
                    await asyncio.sleep(exp)
                    exp += exp_size

        return wrapper  # type: ignore

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])

    return decorator  # type: ignore
