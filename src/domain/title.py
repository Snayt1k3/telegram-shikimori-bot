from dataclasses import dataclass

from src.domain.base import BaseEntity
from src.application.dto.title.title import TitleDTO, TitleUpdateDTO


@dataclass
class TitleEntity(BaseEntity):
    id: int
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
