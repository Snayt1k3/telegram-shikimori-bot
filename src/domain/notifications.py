import datetime
from dataclasses import dataclass
from typing import List
from src.domain.user import UserEntity
from src.domain.base import BaseEntity
from src.application.dto.notifications.notification import (
    NotificationDTO,
    NotificationUpdateDTO,
)


@dataclass
class NotificationEntity(BaseEntity):
    id: int
    ru: str
    en: str
    episode: str
    user: UserEntity
    created_at: datetime.datetime
    is_sended: bool = False

    @classmethod
    def create(cls, obj: NotificationDTO) -> "NotificationEntity":
        return cls(
            id=obj.id,
            user=UserEntity.create(obj.user),
            is_sended=obj.is_sended,
            ru=obj.ru,
            en=obj.en,
            episode=obj.episode,
            created_at=datetime.datetime.utcnow(),
        )

    def update(self, data: NotificationUpdateDTO) -> "NotificationEntity":
        self.is_sended = data.is_sended
        return self
