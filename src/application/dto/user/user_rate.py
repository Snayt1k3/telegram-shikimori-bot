import dataclasses
from typing import Optional

from src.application.dto.title.title import TitleDTO, TitleUpdateDTO


@dataclasses.dataclass
class UserRateDTO:
    id: int
    user_id: int
    title: TitleDTO
    episodes: int
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]


@dataclasses.dataclass
class UserRateUpdateDTO:
    title: TitleUpdateDTO
    episodes: int
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]
