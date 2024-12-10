from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.base import Entity


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs) -> int:
        """Добавить новую сущность в хранилище."""
        pass

    @abstractmethod
    async def add_many(self, objs: list[dict]) -> list[int]:
        """Добавить новые сущности в хранилище."""
        pass

    @abstractmethod
    async def edit_one(self, **kwargs) -> Entity:
        """Обновить сущность в хранилище."""
        pass

    @abstractmethod
    async def delete_one(self, entity_id: int) -> int | None:
        """Удалить сущность из хранилища по ее ID."""
        pass

    @abstractmethod
    async def delete_many(self, ids: list[int]) -> list[int] | None:
        """Удалить сущности из хранилища по их ID."""
        pass

    @abstractmethod
    async def find_all(self) -> list[Entity]:
        """Вернуть список всех сущностей."""
        pass

    @abstractmethod
    async def find_one(self, **kwargs) -> Optional[Entity]:
        """Отфильтровать сущности по заданным критериям."""
        pass

    @abstractmethod
    async def find_many(self, **kwargs) -> list[Entity]:
        """Отфильтровать сущности по заданным критериям."""
        pass

    @abstractmethod
    async def update_one(self, id: int, **kwargs) -> Entity:
        """Обновляет сущность по заданным критериям."""
        pass
