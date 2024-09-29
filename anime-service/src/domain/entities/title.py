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

    def update(self, data: Any) -> None:
        self.title_ru = data.title_ru
        self.title_en = data.title_en
        self.image_url = data.image_url
        self.status = data.status
        self.score = data.score
        self.episodes = data.episodes
        self.episodes_aired = data.episodes_aired
        self.volumes = data.volumes
        self.chapters = data.chapters

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
