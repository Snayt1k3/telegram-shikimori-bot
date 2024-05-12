import dataclasses
import datetime
from typing import List

from src.dto.base import DTO
from src.dto.user.user import UserUpdateDTO, UserDTO


@dataclasses.dataclass
class AnimeAlDTO(DTO):
    id: int
    ru: str
    en: str
    voicers: List[str]
    episode: int
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "AnimeAlDTO":
        return cls(
            id=data.get("id"),
            ru=data.get("ru"),
            en=data.get("en"),
            voicers=data.get("voicers"),
            episode=data.get("episode"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ru": self.ru,
            "en": self.en,
            "episode": self.episode,
            "created_at": self.created_at,
            "voicers": self.voicers,
        }


@dataclasses.dataclass
class NotificationDTO(DTO):
    id: int
    anime: AnimeAlDTO
    user: UserDTO
    is_sended: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationDTO":
        return cls(
            id=data.get("id"),
            anime=AnimeAlDTO.from_dict(data.get("anime")),
            user=UserDTO.from_dict(data.get("data")),
            is_sended=data.get("is_sended"),
        )

    def to_dict(self) -> dict:
        return {
            "is_sended": self.is_sended,
            "id": self.id,
            "anime": self.anime.to_dict(),
            "user": self.user.to_dict(),
        }


@dataclasses.dataclass
class NotificationUpdateDTO(DTO):
    id: int
    anime: AnimeAlDTO
    # user: UserUpdateDTO
    is_sended: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationUpdateDTO":
        return cls(
            id=data.get("id"),
            anime=AnimeAlDTO.from_dict(data.get("anime")),
            # user=UserUpdateDTO.from_dict(data.get("user")),
            is_sended=data.get("is_sended"),
        )

    def to_dict(self) -> dict:
        return {
            "is_sended": self.is_sended,
            "id": self.id,
            "anime": self.anime.to_dict(),
            # "user": self.user.to_dict(),
        }
