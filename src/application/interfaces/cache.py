from abc import ABC


class AbstractCache(ABC):
    """
    Interface for cache tools
    """

    async def get(self, key: str):
        raise NotImplementedError

    async def set(self, key: str, data: dict | list, expire_in: int = 60 * 60):
        raise NotImplementedError

    async def delete(self, key: str):
        raise NotImplementedError
