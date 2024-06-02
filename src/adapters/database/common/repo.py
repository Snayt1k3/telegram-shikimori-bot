from dataclasses import asdict
from typing import Generic, TypeVar

from sqlalchemy import update, select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractMapper, AbstractRepository

Entity = TypeVar("Entity")


class SQLAlchemyRepository(AbstractRepository[Entity], Generic[Entity]):
    model = None

    def __init__(self, session: AsyncSession, mapper: AbstractMapper):
        self.session = session
        self.mapper = mapper

    async def add_one(self, entity: Entity) -> Entity:
        stmt = insert(self.model).values(**asdict(entity)).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def edit_one(self, entity: Entity) -> Entity:
        stmt = update(self.model).values(**asdict(entity)).filter_by(id=entity.id).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self) -> list[Entity]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by) -> Entity:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def delete_one(self, id: int) -> Entity:
        stmt = delete(self.model).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())
