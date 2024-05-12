from dataclasses import dataclass
from typing import Optional

from src.domain.base import BaseEntity
from src.domain.title import TitleEntity
from src.dto.user.user_rate import UserRateDTO, UserRateUpdateDTO


@dataclass
class UserRateEntity(BaseEntity):
    id: int
    user_id: int
    title: TitleEntity
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    @classmethod
    def create(cls, obj: UserRateDTO) -> "UserRateEntity":
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            title=TitleEntity.create(obj.title),
            episodes=obj.episodes,
            target_id=obj.target_id,
            target_type=obj.target_type,
            score=obj.score,
            status=obj.status,
            chapters=obj.chapters,
            volumes=obj.volumes,
            rewatches=obj.rewatches,
        )

    def update(self, data: UserRateUpdateDTO) -> "UserRateEntity":
        self.title.update(data.title)
        self.score = data.score
        self.episodes = data.episodes
        self.status = data.status
        self.chapters = data.chapters
        self.volumes = data.volumes
        self.rewatches = data.rewatches

        return self
