import dataclasses
from typing import List
from typing import Optional

from src.application.dto.title.title import TitleDTO
from src.application.dto.user.auth import ShikiCredsDTO
from src.application.enums import ShikimoriListType


@dataclasses.dataclass
class UserDTO:
    id: int
    id_telegram: int
    nickname: str
    avatar: str
    user_rates: List["UserRateDTO"]
    creds: ShikiCredsDTO
    follows: list[int]
    allow_notifications: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "UserDTO":
        return cls(
            id=data["id"],
            id_telegram=data["id_telegram"],
            nickname=data["nickname"],
            avatar=data["avatar"],
            user_rates=[UserRateDTO.from_dict(rate) for rate in data["user_rates"]],
            creds=ShikiCredsDTO.from_dict(data["creds"]),
            allow_notifications=data.get("allow_notifications", True),
            follows=data.get("follows"),
        )


@dataclasses.dataclass
class UserUpdateDTO:
    nickname: str
    avatar: str
    allow_notifications: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "UserUpdateDTO":
        return cls(
            nickname=data["nickname"],
            avatar=data["avatar"],
            allow_notifications=data.get("allow_notifications"),
        )


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

    @classmethod
    def from_dict(cls, data: dict) -> "UserRateDTO":
        return cls(
            id=data["id"],
            user=UserDTO.from_dict(data["user"]),
            title=TitleDTO.from_dict(data["title"]),
            episodes=data.get("episodes"),
            target_id=data["target_id"],
            target_type=data["target_type"],
            score=data["score"],
            status=data["status"],
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            rewatches=data.get("rewatches"),
        )

@dataclasses.dataclass
class UserCreateDTO:
    target_id: int
    target_type: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "UserCreateDTO":
        return cls(
            target_id=data["target_id"],
            target_type=data["target_type"],
            status=data["status"],
        )

@dataclasses.dataclass
class UserRateUpdateDTO:
    id: int
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "UserRateUpdateDTO":
        return cls(
            id=data["id"],
            score=data["score"],
            status=data["status"],
            episodes=data.get("episodes"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            rewatches=data.get("rewatches"),
        )

@dataclasses.dataclass
class UserListDTO:
    """
    obj which represents a shikimori list
    """

    objs: list[UserRateDTO]
    type: ShikimoriListType
    length: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            objs=[UserRateDTO.from_dict(i) for i in data["objs"]],
            type=ShikimoriListType(data.get("type")),
            length=data.get("length"),
        )
