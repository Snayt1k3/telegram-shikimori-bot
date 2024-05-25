import dataclasses
from typing import Optional


@dataclasses.dataclass
class TitleDTO:
    id: int
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: str
    episodes: int
    episodes_aired: int
    chapters: int
    volumes: int


@dataclasses.dataclass
class TitleUpdateDTO:
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: str
    episodes: Optional[int]
    episodes_aired: Optional[int]
    volumes: Optional[int]
    chapters: Optional[int]


