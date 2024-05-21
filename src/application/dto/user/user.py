import dataclasses
from typing import List
from src.application.dto.user.user_rate import UserRateDTO, UserRateUpdateDTO


@dataclasses.dataclass
class UserDTO:
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List[UserRateDTO]
    allow_notifications: bool = True


@dataclasses.dataclass
class UserUpdateDTO:
    nickname: str
    avatar: str
    user_rates: List[UserRateUpdateDTO]
    allow_notifications: bool = True

