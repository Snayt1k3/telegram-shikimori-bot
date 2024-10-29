import dataclasses
from typing import Any

from src.domain.entities.base import Entity


@dataclasses.dataclass
class TitleEntity(Entity):
    id: int
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: float
    episodes: int
    episodes_aired: int
    volumes: int
    chapters: int

    @classmethod
    def create(
        cls,
        id: int,
        title_ru: str,
        title_en: str,
        image_url: str,
        status: str,
        score: int,
        episodes: int,
        episodes_aired: int,
        volumes: int,
        chapters: int,
    ):
        return cls(
            id=id,
            title_ru=title_ru,
            title_en=title_en,
            image_url=image_url,
            status=status,
            score=score,
            episodes=episodes,
            episodes_aired=episodes_aired,
            volumes=volumes,
            chapters=chapters,
        )
