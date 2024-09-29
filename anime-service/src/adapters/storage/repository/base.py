from dataclasses import asdict
from typing import Optional

from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractRepository
from src.application.interfaces.mapper import AbstractMapper
from src.domain.entities.base import Entity


class SQLAlchemyRepository(AbstractRepository):
    model = None
    mapper: AbstractMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, entity: Entity) -> int:
        stmt = insert(self.model).values(asdict(entity)).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, entity: Entity) -> Entity:
        stmt = (
            update(self.model)
            .values(asdict(entity))
            .filter_by(id=entity.id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self) -> list:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by) -> Optional[Entity]:
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
