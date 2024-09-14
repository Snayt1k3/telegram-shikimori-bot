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

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationDTO":
        return cls(
            id=data.get("id"),
            episode=data.get("episode"),
            en=data.get("en"),
            is_sended=data.get("is_sended"),
            created_at=datetime.datetime.fromtimestamp(data.get("created_at")),
            ru=data.get("ru"),
            user=UserDTO.from_dict(data.get("user")),
        )
