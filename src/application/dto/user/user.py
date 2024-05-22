import dataclasses
from typing import List
from typing import Optional

from src.application.dto.title.title import TitleDTO


class ShikiCredsDTO:
    id: int
    access: str
    refresh: str
    expire_in: str


@dataclasses.dataclass
class UserDTO:
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List["UserRateDTO"]
    creds: ShikiCredsDTO
    allow_notifications: bool = True


@dataclasses.dataclass
class UserCreateDTO:
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List["UserRateDTO"]
    creds: ShikiCredsDTO
    allow_notifications: bool = True


@dataclasses.dataclass
class UserUpdateDTO:
    nickname: str
    avatar: str
    allow_notifications: bool = True


@dataclasses.dataclass
class UserRateDTO:
    id: int
    user: UserDTO
    title: TitleDTO
    episodes: int
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]


@dataclasses.dataclass
class UserRateUpdateDTO:
    id: int
    episodes: int
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]
