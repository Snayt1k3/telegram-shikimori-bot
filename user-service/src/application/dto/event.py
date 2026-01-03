from typing import TypedDict, Any

from pydantic import BaseModel


class User(BaseModel):
    id: int
    shikimori_id: int
    token: str

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id"),
            shikimori_id=data.get("shikimori_id"),
            token=data.get("token"),
        )


class Event(BaseModel):
    event_type: str
    correlation_id: str
    data: dict | None
    user_info: User | None

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        user = data.get("user_info")
        return cls(
            event_type=data.get("event_type"),
            correlation_id=data.get("correlation_id"),
            data=data.get("data"),
            user_info=User.from_dict(user) if user else None,
        )


class EventResponse(BaseModel):
    error: str | None
    data: dict | None
    correlation_id: str
    status_code: int


class ResponseDTO(TypedDict):
    error: str | None
    data: Any
    status: int
