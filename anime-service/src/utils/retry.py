import asyncio
import time
from functools import wraps
from logging import getLogger
from typing import Callable, Type, Tuple, Union

logger = getLogger(__name__)

def retry(
    exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = Exception,
    tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
):
    """
    Декоратор для повторного выполнения функции при исключении.

    :param exceptions: Исключения, при которых повторяем
    :param tries: количество попыток
    :param delay: задержка перед первой повторной попыткой
    :param backoff: множитель для увеличения задержки после каждой ошибки
    """
    def decorator(func: Callable):
        is_async = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    print(f"[retry] Exception: {e}, retrying in {_delay:.1f}s...")
                    await asyncio.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"[retry] Exception: {e}, retrying in {_delay:.1f}s...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)

        return async_wrapper if is_async else sync_wrapper

    return decorator
