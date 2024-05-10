from dataclasses import dataclass
from typing import Optional

from src.domain.base import BaseEntity


@dataclass
class UserRateEntity(BaseEntity):
    id: Optional[str]
    shikimori_id: int
    anime_id: int




    @classmethod
    def create(cls, obj) -> "UserRateEntity":
        pass

    def update(self, data) -> "UserRateEntity":
        pass
