import uuid
from typing import Literal

from pydantic import BaseModel
from src.dto import AuthenticatedUser


class MQMessage(BaseModel):
    correlation_id: uuid.UUID
    event_type: Literal[
        "add_rate",
        "read_rates",
        "read_titles",
        "update_rate",
        "delete_rate",
        "load_rates",
        "get_profile",
    ]
    data: dict | None
    user_info: AuthenticatedUser | None

    def to_dict(self) -> dict:
        return {
            "correlation_id": str(self.correlation_id),
            "event_type": self.event_type,
            "data": self.data,
            "user_info": self.user_info.model_dump() if self.user_info else None,
        }
