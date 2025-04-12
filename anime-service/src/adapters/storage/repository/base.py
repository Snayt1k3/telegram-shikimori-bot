from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs: dict) -> model:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def add_many(self, objs: list[dict]) -> list[int]:
        """Добавить новые сущности в хранилище."""
        stmt = insert(self.model).values(objs).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()  # type: ignore

    async def edit_one(self, id: int, **kwargs: dict) -> model:
        stmt = (
            update(self.model).values(**kwargs).filter_by(id=id).returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self) -> list[model]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def find_one(self, **filter_by: dict) -> model:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()

        if res is None:
            return None

        return res

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_many(self, ids: [int]) -> list[int]:
        stmt = delete(self.model).where(self.model.id.in_(ids)).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()  # type: ignore

    async def find_many(self, **filters) -> list[model]:
        stmt = select(self.model)

        for key, value in filters.items():
            if "__icontains" in key:
                field = getattr(self.model, key.replace("__icontains", ""))
                stmt = stmt.where(field.ilike(f"%{value}%"))
            elif "__in" in key:
                field = getattr(self.model, key.replace("__in", ""))
                stmt = stmt.where(field.in_(value))
            else:
                field = getattr(self.model, key)
                stmt = stmt.where(field == value)  # type: ignore

        res = await self.session.execute(stmt)
        return [row[0] for row in res.all()]

    async def update_one(self, id: int, **kwargs) -> model:
        """Обновляет одну сущность по ID."""
        stmt = (
            update(self.model)
            .where(self.model.id == id)  # type: ignore
            .values(**kwargs)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
