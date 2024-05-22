import dataclasses
import datetime

from src.application.dto.user.user import UserDTO


@dataclasses.dataclass
class NotificationDTO:
    id: int
    en: str
    ru: str
    episode: str
    user: UserDTO
    created_at: datetime.datetime
    is_sended: bool = False


@dataclasses.dataclass
class NotificationUpdateDTO:
    id: int
    is_sended: bool = False


@dataclasses.dataclass
class NotificationCreateDTO:
    user_id: int
    id: int
    en: str
    ru: str
    episode: str
    is_sended: bool = False
