import uuid
from typing import Literal

from pydantic import BaseModel

from src.dto import User


class MQMessage(BaseModel):
    correlation_id: uuid.UUID
    event_type: Literal[
        "read_rate",
        "delete_rates",
        "delete_rate",
        "update_rate",
        "update_rates",
        "read_rates",
        "add_rate",
        "add_rates",
        "read_title",
        "read_titles",
    ]
    data: dict
    user_info: User

    def to_dict(self) -> dict:
        return {
            "correlation_id": self.correlation_id,
            "event_type": self.event_type,
            "data": self.data,
            "user_info": self.user_info.model_dump(),
        }
