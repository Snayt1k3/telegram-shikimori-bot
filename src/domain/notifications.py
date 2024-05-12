import datetime
from dataclasses import dataclass
from typing import List
from src.domain.user import UserEntity
from src.domain.base import BaseEntity
from src.dto.notifications.notification import NotificationDTO, NotificationUpdateDTO


@dataclass
class AnimeAL:
    id: int
    ru: str
    en: str
    voicers: List[str]
    episode: int
    created_at: datetime.datetime


@dataclass
class NotificationEntity(BaseEntity):
    id: int
    anime: AnimeAL
    user: UserEntity
    is_sended: bool = False

    @classmethod
    def create(cls, obj: NotificationDTO) -> "NotificationEntity":
        return cls(
            id=obj.id,
            anime=AnimeAL(**obj.anime.to_dict()),
            user=UserEntity.create(obj.user),
            is_sended=obj.is_sended,
        )

    def update(self, data: NotificationUpdateDTO) -> "NotificationEntity":
        self.anime = AnimeAL(**data.anime.to_dict())
        self.is_sended = data.is_sended
        return self
