from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractRepository
from src.application.interfaces.mapper import AbstractMapper


class SQLAlchemyRepository(AbstractRepository):
    model = None
    mapper: AbstractMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs: dict) -> int:
        stmt = insert(self.model).values(**kwargs).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def add_many(self, objs: list[dict]) -> list[int]:
        """Добавить новые сущности в хранилище."""
        stmt = insert(self.model).values(objs).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def edit_one(self, id: int, **kwargs: dict):
        stmt = (
            update(self.model).values(**kwargs).filter_by(id=id).returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self) -> list:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by: dict):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is None:
            return None

        return self.mapper.model_to_entity(res)

    async def delete_one(self, id: int):
        stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_many(self, ids: [int]) -> list[int]:
        stmt = delete(self.model).where(self.model.id.in_(ids)).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_many(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return [self.mapper.model_to_entity(row[0]) for row in res.all()]

    async def update_one(self, id: int, **kwargs):
        """Обновляет одну сущность по ID."""
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
