import dataclasses


@dataclasses.dataclass
class NotificationUpdateDTO:
    id: int
    is_sended: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationUpdateDTO":
        return cls(
            id=data.get("id"),
            is_sended=data.get("is_sended"),
        )
