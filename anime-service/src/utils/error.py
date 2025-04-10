from functools import wraps
from logging import getLogger
from typing import Callable, Awaitable, Any

logger = getLogger(__name__)


def error_handler(task_name: str):
    def decorator(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"Start processing '{task_name}'")

                result = await func(*args, **kwargs)

                logger.info(f"Processing complete '{task_name}'")

                return result
            except Exception as e:
                logger.error(f"Error occurred while processing '{task_name}': {str(e)}")
                return {"status": 500, "data": None, "error": str(e)}

        return wrapper

    return decorator
