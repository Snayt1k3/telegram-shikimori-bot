from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession


class BaseSqlRepository(ABC):
    """
    interface for sql database repository
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, new_data):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, obj):
        raise NotImplementedError
