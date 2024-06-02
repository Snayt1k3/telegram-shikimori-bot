import datetime
from dataclasses import dataclass
from typing import Optional

from src.application.dto.notifications.notification import (
    NotificationUpdateDTO,
)
from src.domain.base import BaseEntity
from src.domain.user import UserEntity


@dataclass
class NotificationEntity(BaseEntity):
    id: Optional[int]
    ru: str
    en: str
    episode: int
    user: UserEntity
    created_at: datetime.datetime
    is_sended: bool = False

    def update(self, data: NotificationUpdateDTO) -> "NotificationEntity":
        self.is_sended = data.is_sended
        return self

    @classmethod
    def create(
        cls,
        ru: str,
        en: str,
        episode: int,
        user: UserEntity,
        created_at: datetime.datetime,
    ) -> "NotificationEntity":
        return cls(
            id=None,
            ru=ru,
            en=en,
            episode=episode,
            user=user,
            created_at=created_at,
        )
