from abc import ABC


class AbstractCache(ABC):
    """
    Interface for cache tools
    """

    def __init__(self, client):
        self.client = client

    async def get(self, key: str, namespace: str):
        raise NotImplementedError

    async def set(self, key: str, namespace: str, data: dict, expire_in: int = 60 * 60):
        raise NotImplementedError
