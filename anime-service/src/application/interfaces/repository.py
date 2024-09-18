from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, entity):
        """Добавить новую сущность в хранилище."""
        pass

    @abstractmethod
    async def edit_one(self, entity):
        """Обновить сущность в хранилище."""
        pass

    @abstractmethod
    async def delete_one(self, entity_id: int):
        """Удалить сущность из хранилища по ее ID."""
        pass

    @abstractmethod
    async def find_all(self):
        """Вернуть список всех сущностей."""
        pass

    @abstractmethod
    async def find_one(self, **kwargs):
        """Отфильтровать сущности по заданным критериям."""
        pass
