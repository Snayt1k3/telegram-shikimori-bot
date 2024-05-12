from dataclasses import dataclass
from typing import Optional, List
from src.domain.user_rate import UserRateEntity
from src.domain.base import BaseEntity
from src.dto.base import DTO
from src.dto.user.user import UserUpdateDTO, UserDTO


@dataclass
class UserEntity(BaseEntity):
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List[UserRateEntity]
    allow_notifications: bool = True

    @classmethod
    def create(cls, obj: UserDTO) -> "UserEntity":
        return cls(
            id=obj.id,
            id_telegram=obj.id_telegram,
            avatar=obj.avatar,
            user_rates=[UserRateEntity.create(rate) for rate in obj.user_rates],
            allow_notifications=obj.allow_notifications,
            nickname=obj.nickname,
        )

    def update(self, data: UserUpdateDTO) -> "UserEntity":
        self.nickname = data.nickname
        self.avatar = data.avatar
        self.allow_notifications = data.allow_notifications
        # self.user_rates = [UserRateEntity.create(rate) for rate in data.user_rates]  # TODO сделать обновление

        return self
