from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.base import Entity


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, entity: Entity) -> int:
        """Добавить новую сущность в хранилище."""
        pass

    @abstractmethod
    async def edit_one(self, entity: Entity) -> Entity:
        """Обновить сущность в хранилище."""
        pass

    @abstractmethod
    async def delete_one(self, entity_id: int) -> int:
        """Удалить сущность из хранилища по ее ID."""
        pass

    @abstractmethod
    async def find_all(self) -> list[Entity]:
        """Вернуть список всех сущностей."""
        pass

    @abstractmethod
    async def find_one(self, **kwargs) -> Optional[Entity]:
        """Отфильтровать сущности по заданным критериям."""
        pass
