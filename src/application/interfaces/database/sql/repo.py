from abc import ABC, abstractmethod
from typing import TypeVar, Generic

Entity = TypeVar("Entity")

class AbstractRepository(ABC, Generic[Entity]):
    @abstractmethod
    async def add_one(self, entity: Entity) -> Entity:
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, entity: Entity) -> Entity:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[Entity]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by) -> Entity:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> Entity:
        raise NotImplementedError
