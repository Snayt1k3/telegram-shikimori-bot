from sqlalchemy import select, insert, update
from sqlalchemy.orm import joinedload

from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.user.orm import User, UserRate, ShikiCredential
from src.domain.user import UserEntity, UserRateEntity, ShikiCredsEntity


class UserRepository(SQLAlchemyRepository[UserEntity]):
    model = User

    async def add_one(self, entity: UserEntity) -> int:
        stmt = (
            insert(self.model)
            .values(
                id_telegram=entity.id_telegram,
                id=entity.id,
                nickname=entity.nickname,
                cred_id=entity.creds.id,
                avatar=entity.avatar,
                allow_notifications=entity.allow_notifications,
                follows=entity.follows,
            )
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.unique().scalar_one()

    async def edit_one(self, entity: UserEntity) -> UserEntity:
        stmt = (
            update(self.model)
            .values(
                id_telegram=entity.id_telegram,
                id=entity.id,
                nickname=entity.nickname,
                cred_id=entity.creds.id,
                avatar=entity.avatar,
                allow_notifications=entity.allow_notifications,
                follows=entity.follows,
                user_rates=entity.user_rates,
            )
            .filter_by(id=entity.id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self):
        stmt = select(self.model).options(joinedload(self.model.creds))
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.creds))
        )
        res = await self.session.execute(stmt)
        res = res.unique().scalar_one()
        return self.mapper.model_to_entity(res)


class UserRateRepository(SQLAlchemyRepository[UserRateEntity]):
    model = UserRate

    async def add_one(self, entity: UserRateEntity) -> int:
        stmt = (
            insert(self.model)
            .values(
                id=entity.id,
                user_id=entity.user_id,
                title_id=entity.title.id,
                target_id=entity.target_id,
                target_type=entity.target_type,
                score=entity.score,
                status=entity.status,
                episodes=entity.episodes,
                volumes=entity.volumes,
                chapters=entity.chapters,
                rewatches=entity.rewatches,
            )
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, entity: UserRateEntity) -> UserRateEntity:
        stmt = (
            update(self.model)
            .values(
                target_id=entity.target_id,
                target_type=entity.target_type,
                score=entity.score,
                status=entity.status,
                episodes=entity.episodes,
                volumes=entity.volumes,
                chapters=entity.chapters,
                rewatches=entity.rewatches,
            )
            .filter_by(id=entity.id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self):
        stmt = select(self.model).options(joinedload(self.model.title))
        res = await self.session.execute(stmt)
        res = [self.mapper.model_to_entity(row[0]) for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.title))
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return self.mapper.model_to_entity(res)


class ShikiCredsRepository(SQLAlchemyRepository[ShikiCredsEntity]):
    model = ShikiCredential

    async def add_one(self, entity: ShikiCredsEntity) -> int:
        stmt = (
            insert(self.model)
            .values(
                access=entity.access,
                refresh=entity.refresh,
                expire_in=entity.expire_in,
            )
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
