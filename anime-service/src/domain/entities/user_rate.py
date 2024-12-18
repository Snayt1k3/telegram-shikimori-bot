import dataclasses

from src.domain.entities.base import Entity
from src.domain.entities.title import TitleEntity


@dataclasses.dataclass
class UserRateEntity(Entity):
    id: int
    title: TitleEntity
    target_id: int
    target_type: str
    status: str
    score: float
    episodes: int
    rewatches: int
    volumes: int
    chapters: int

    @classmethod
    def create(
        cls,
        id: int,
        target_type: str,
        status: str,
        score: int,
        episodes: int,
        rewatches: int,
        volumes: int,
        chapters: int,
        title: TitleEntity,
    ):
        return cls(
            id=id,
            status=status,
            score=score,
            episodes=episodes,
            volumes=volumes,
            chapters=chapters,
            target_type=target_type,
            rewatches=rewatches,
            title=title,
        )
