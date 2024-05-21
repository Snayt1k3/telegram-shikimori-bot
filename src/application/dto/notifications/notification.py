import dataclasses
from typing import List

from src.application.dto.user.user import UserDTO


@dataclasses.dataclass
class AnimeAlDTO:
    id: int
    ru: str
    en: str
    voicers: List[str]
    episode: int
    created_at: str


@dataclasses.dataclass
class NotificationDTO:
    id: int
    anime: AnimeAlDTO
    user: UserDTO
    is_sended: bool = False


@dataclasses.dataclass
class NotificationUpdateDTO:
    is_sended: bool = False


@dataclasses.dataclass
class NotificationCreateDTO:
    anime: AnimeAlDTO
    user_id: int
    is_sended: bool = False

