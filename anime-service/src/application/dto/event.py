from pydantic import BaseModel


class User(BaseModel):
    id_telegram: int
    shikimori_id: int

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id_telegram=data.get("id_telegram"), shikimori_id=data.get("shikimori_id")
        )


class Event(BaseModel):
    event_type: str
    correlation_id: int
    data: dict
    user_info: User

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            event_type=data.get("event_type"),
            correlation_id=data.get("correlation_id"),
            data=data.get("data"),
            user_info=User.from_dict(data.get("user_info")),
        )


class EventResponse(BaseModel):
    error: str | None
    data: dict
    correlation_id: int
    status_code: int
