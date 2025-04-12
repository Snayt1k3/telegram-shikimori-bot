from abc import ABC, abstractmethod
from typing import Optional


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs) -> int:
        """Добавить новую сущность в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, objs: list[dict]) -> list[int]:
        """Добавить новые сущности в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, **kwargs):
        """Обновить сущность в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, obj_id: int) -> int | None:
        """Удалить сущность из хранилища по ее ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, ids: list[int]) -> list[int] | None:
        """Удалить сущности из хранилища по их ID."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list:
        """Вернуть список всех сущностей."""
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **kwargs) -> Optional:
        """Отфильтровать сущности по заданным критериям."""
        raise NotImplementedError

    @abstractmethod
    async def find_many(self, **filters) -> list:
        """
        Отфильтровать сущности по заданным критериям.

        Поддерживаемые параметры фильтрации:
        - field=value: точное совпадение (например, status="ongoing")
        - field__icontains=value: частичное совпадение без учёта регистра (например, title_en__icontains="naruto")
        - field__in=[v1, v2, ...]: значение поля входит в указанный список (например, id__in=[1, 2, 3])
        """
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, **kwargs):
        """Обновляет сущность по заданным критериям."""
        raise NotImplementedError
