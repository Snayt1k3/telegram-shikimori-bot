from src.application.interfaces.database.sql.mapper import AbstractMapper
from src.domain.notifications import NotificationEntity
from src.adapters.database.sql.notifications.orm import Notification
from src.adapters.database.sql.user.mapper import UserMapper

class NotificationMapper(AbstractMapper):
    @staticmethod
    def entity_to_model(model: NotificationEntity) -> Notification:
        return Notification(
            id=model.id,
            ru=model.ru,
            en=model.en,
            episode=model.episode,
            user=UserMapper.entity_to_model(model.user),
            created_at=model.created_at,
        )

    @staticmethod
    def model_to_entity(model: Notification) -> NotificationEntity:
        return NotificationEntity(
            id=model.id,
            ru=model.ru,
            en=model.en,
            episode=model.episode,
            user=UserMapper.model_to_entity(model.user),
            created_at=model.created_at,
        )
