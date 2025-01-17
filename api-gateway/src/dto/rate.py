from typing import Literal

from pydantic import BaseModel


class RateUpdateDTO(BaseModel): ...


class RateFilterDTO(BaseModel):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    user_id: int = None

    def to_dict(self) -> dict:
        res = {}
        if self.status:
            res["status"] = self.status

        if self.user_id:
            res["user_id"] = self.user_id

        return res
