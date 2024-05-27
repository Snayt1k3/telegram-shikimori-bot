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

    @classmethod
    def from_dict(cls, data: dict) -> "TitleDTO":
        return cls(
            id=data["id"],
            title_ru=data["title_ru"],
            title_en=data["title_en"],
            image_url=data["image_url"],
            status=data["status"],
            score=data["score"],
            episodes=data["episodes"],
            episodes_aired=data["episodes_aired"],
            chapters=data["chapters"],
            volumes=data["volumes"]
        )


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


