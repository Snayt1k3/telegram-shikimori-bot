from dataclasses import dataclass
from typing import Optional

from src.application.dto.title.title import TitleUpdateDTO
from src.domain.base import BaseEntity


@dataclass
class TitleEntity(BaseEntity):
    id: Optional[int]
    target_id: int
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: str
    episodes: int
    episodes_aired: int
    volumes: int
    chapters: int

    def update(self, data: TitleUpdateDTO) -> "TitleEntity":
        self.title_ru = data.title_ru
        self.title_en = data.title_en
        self.image_url = data.image_url
        self.status = data.status
        self.score = data.score
        self.episodes = data.episodes
        self.episodes_aired = data.episodes_aired
        self.volumes = data.volumes
        self.chapters = data.chapters

        return self

    @classmethod
    def create(
        cls,
        target_id,
        title_ru,
        title_en,
        image_url,
        status,
        score,
        episodes,
        episodes_aired,
        volumes,
        chapters,
    ):
        return cls(
            id=None,
            target_id=target_id,
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
