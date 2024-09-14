import dataclasses


@dataclasses.dataclass
class NotificationCreateDTO:
    user_id: int
    id: int
    en: str
    ru: str
    episode: str
    is_sended: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationCreateDTO":
        return cls(
            id=data.get("id"),
            episode=data.get("episode"),
            en=data.get("en"),
            is_sended=data.get("is_sended"),
            ru=data.get("ru"),
            user_id=data.get("user_id"),
        )