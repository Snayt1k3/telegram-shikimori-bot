import dataclasses
from typing import Optional

from src.application.dto.base import DTO


@dataclasses.dataclass
class TitleDTO(DTO):
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
            id=data.get("id"),
            title_ru=data.get("title_ru"),
            title_en=data.get("title_en"),
            status=data.get("status"),
            score=data.get("score"),
            episodes_aired=data.get("episodes_aired"),
            episodes=data.get("episodes"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            image_url=data.get("image_url"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title_ru": self.title_ru,
            "title_en": self.title_en,
            "image_url": self.image_url,
            "status": self.status,
            "score": self.score,
            "episodes": self.episodes,
            "volumes": self.volumes,
            "chapters": self.chapters,
            "episodes_aired": self.episodes_aired,
        }


@dataclasses.dataclass
class TitleUpdateDTO(DTO):
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: str
    episodes: Optional[int]
    episodes_aired: Optional[int]
    volumes: Optional[int]
    chapters: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "TitleUpdateDTO":
        return cls(
            title_ru=data.get("title_ru"),
            title_en=data.get("title_en"),
            status=data.get("status"),
            score=data.get("score"),
            episodes_aired=data.get("episodes_aired"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            episodes=data.get("episodes"),
            image_url=data.get("image_url"),
        )

    def to_dict(self) -> dict:
        return {
            "title_ru": self.title_ru,
            "title_en": self.title_en,
            "image_url": self.image_url,
            "status": self.status,
            "score": self.score,
            "episodes": self.episodes,
            "chapters": self.chapters,
            "volumes": self.volumes,
            "episodes_aired": self.episodes_aired,
        }
