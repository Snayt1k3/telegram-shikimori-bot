from abc import ABC, abstractmethod
from typing import Optional, Any

from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.storage.models import User


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, **kwargs) -> Any:
        """Добавить новую сущность в хранилище."""
        pass

    @abstractmethod
    async def find_one(self, **kwargs) -> Optional[Any]:
        """Отфильтровать сущности по заданным критериям."""
        pass

    @abstractmethod
    async def update_one(self, id: int, **kwargs) -> Any:
        """Обновляет сущность по заданным критериям."""
        pass


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs: dict) -> model:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update_one(self, id: int, **kwargs: dict):
        stmt = (
            update(self.model).values(**kwargs).filter_by(id=id).returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_one(self, **filter_by: dict) -> Optional[model]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is None:
            return None

        return res


class UserRepo(SQLAlchemyRepository):
    model = User
