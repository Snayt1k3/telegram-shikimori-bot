import datetime
from dataclasses import dataclass

from src.application.dto.notifications.notification import (
    NotificationUpdateDTO,
)
from src.domain.base import BaseEntity
from src.domain.user import UserEntity


@dataclass
class NotificationEntity(BaseEntity):
    id: int
    ru: str
    en: str
    episode: str
    user: UserEntity
    created_at: datetime.datetime
    is_sended: bool = False

    def update(self, data: NotificationUpdateDTO) -> "NotificationEntity":
        self.is_sended = data.is_sended
        return self
