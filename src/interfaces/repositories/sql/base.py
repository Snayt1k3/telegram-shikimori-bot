from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar("T")


class BaseSqlRepository(Generic[T], ABC):
    # TODO create description

    @abstractmethod
    async def get_by_id(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, new_data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, obj: T) -> T:
        raise NotImplementedError
