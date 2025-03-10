from abc import ABC, abstractmethod


class AbstractCache(ABC):
    """
    Interface for cache tools
    """

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, data: dict | list, expire_in: int = 60 * 60):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError
