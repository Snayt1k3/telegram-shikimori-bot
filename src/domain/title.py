from dataclasses import dataclass

from src.domain.base import BaseEntity
from src.dto.title.title import TitleDTO, TitleUpdateDTO


@dataclass
class TitleEntity(BaseEntity):
    id: int
    title_ru: str
    title_en: str
    image_url: str
    status: str
    score: str
    episodes: int
    episodes_aired: int
    volumes: int
    chapters: int

    @classmethod
    def create(cls, obj: TitleDTO) -> "TitleEntity":
        return cls(
            id=obj.id,
            title_ru=obj.title_ru,
            title_en=obj.title_en,
            image_url=obj.image_url,
            status=obj.status,
            score=obj.score,
            episodes=obj.episodes,
            episodes_aired=obj.episodes_aired,
            volumes=obj.volumes,
            chapters=obj.chapters,
        )

    def update(self, data: TitleUpdateDTO) -> "TitleEntity":
        self.title_ru = data.title_ru
        self.title_en = data.title_en
        self.image_url = data.image_url
        self.status = data.status
        self.score = data.score
        self.episodes = data.episodes
        self.episodes_aired = data.episodes_aired

        return self
