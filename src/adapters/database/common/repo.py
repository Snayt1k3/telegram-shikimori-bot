from sqlalchemy import update, select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.database.sql.mapper import AbstractMapper
from src.application.interfaces.database.sql.repo import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession, mapper: AbstractMapper):
        self.session = session
        self.mapper = mapper

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def edit_one(self, id: int, data: dict):
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def delete_one(self, id: int):
        stmt = delete(self.model).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())
