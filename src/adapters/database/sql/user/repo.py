from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.user.orm import User, UserRate, ShikiCredential


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_all(self):
        stmt = select(self.model).options(joinedload(self.model.cred_id))
        res = await self.session.execute(stmt)
        res = [row[0].to_entity() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.cred_id))
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_entity()
        return res


class UserRateRepository(SQLAlchemyRepository):
    model = UserRate

    async def find_all(self):
        stmt = select(self.model).options(
            joinedload(self.model.user_id), joinedload(self.model.title_id)
        )
        res = await self.session.execute(stmt)
        res = [row[0].to_entity() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.user_id), joinedload(self.model.title_id))
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_entity()
        return res


class ShikiCredsRepository(SQLAlchemyRepository):
    model = ShikiCredential
