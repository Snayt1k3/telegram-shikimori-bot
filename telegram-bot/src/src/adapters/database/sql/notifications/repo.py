from sqlalchemy import select, insert, update
from sqlalchemy.orm import joinedload

from src.adapters.database.common.repo import SQLAlchemyRepository
from src.adapters.database.sql.notifications.orm import (
    Notification,
)
from src.application.notifications import NotificationEntity


class NotificationsRepository(SQLAlchemyRepository[NotificationEntity]):
    model = Notification

    async def add_one(self, entity: NotificationEntity) -> NotificationEntity:
        stmt = (
            insert(self.model)
            .values(
                ru=entity.ru,
                en=entity.en,
                episode=entity.episode,
                is_sended=entity.is_sended,
                user_id=entity.user.id,
            )
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def edit_one(self, entity: NotificationEntity) -> NotificationEntity:
        stmt = (
            update(self.model)
            .values(is_sended=entity.is_sended)
            .filter_by(id=entity.id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.mapper.model_to_entity(res.scalar_one())

    async def find_all(self):
        stmt = select(self.model).options(joinedload(self.model.user_id))
        res = await self.session.execute(stmt)
        res = [row[0].to_entity() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.user_id))
        )
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_entity()
        return res
