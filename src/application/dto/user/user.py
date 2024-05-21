import dataclasses
from typing import List
from src.application.dto.user.user_rate import UserRateDTO, UserRateUpdateDTO
from src.application.dto.base import DTO


@dataclasses.dataclass
class UserDTO(DTO):
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List[UserRateDTO]
    allow_notifications: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "UserDTO":
        return cls(
            id=data.get("id"),
            id_telegram=data.get("id_telegram"),
            nickname=data.get("nickname"),
            avatar=data.get("avatar"),
            user_rates=[UserRateDTO.from_dict(rate) for rate in data.get("user_rates")],
            allow_notifications=data.get("allow_notifications"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_telegram": self.id_telegram,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "user_rates": [rate.to_dict() for rate in self.user_rates],
            "allow_notifications": self.allow_notifications,
        }


@dataclasses.dataclass
class UserUpdateDTO(DTO):
    nickname: str
    avatar: str
    user_rates: List[UserRateUpdateDTO]
    allow_notifications: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "UserUpdateDTO":
        return cls(
            nickname=data.get("nickname"),
            avatar=data.get("avatar"),
            user_rates=[UserRateUpdateDTO.from_dict(rate) for rate in data.get("user_rates")],
            allow_notifications=data.get("allow_notifications"),
        )

    def to_dict(self) -> dict:
        return {
            "nickname": self.nickname,
            "avatar": self.avatar,
            "user_rates": [rate.to_dict() for rate in self.user_rates],
            "allow_notifications": self.allow_notifications,
        }
