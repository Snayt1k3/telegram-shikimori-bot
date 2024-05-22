from dataclasses import dataclass
from typing import List

from black import Optional

from src.domain.base import BaseEntity
from src.domain.title import TitleEntity
from src.application.dto.user.user import UserUpdateDTO, UserDTO, ShikiCredsDTO, UserRateDTO, UserRateUpdateDTO


@dataclass
class ShikiCredsEntity(BaseEntity):
    id: int
    access: str
    refresh: str
    expire_in: str

    def is_expired(self) -> bool:
        """Checking creds expire time"""
        # todo сделать логику проверки токена
        pass

    def update_creds(self, data: ShikiCredsDTO) -> "ShikiCredsEntity":
        self.refresh = data.refresh
        self.access = data.access
        self.expire_in = data.expire_in

        return self


@dataclass
class UserEntity(BaseEntity):
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    creds: ShikiCredsEntity
    user_rates: List["UserRateEntity"]
    allow_notifications: bool = True

    def update_user(self, user: UserUpdateDTO) -> None:
        self.avatar = user.avatar
        self.nickname = user.nickname
        self.allow_notifications = user.allow_notifications

    def update_user_rate(self, user_rate: UserRateUpdateDTO) -> None:
        for rate in self.user_rates:
            if rate.id == user_rate.id:
                rate.update(user_rate)
                return

    def update_creds(self, creds: ShikiCredsDTO) -> None:
        self.creds.update_creds(creds)

@dataclass
class UserRateEntity(BaseEntity):
    id: int
    user: UserEntity
    title: TitleEntity
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    def update(self, new: UserRateUpdateDTO):
        self.score = new.score
        self.status = new.status
        self.chapters = new.chapters
        self.rewatches = new.rewatches
        self.episodes = new.episodes
