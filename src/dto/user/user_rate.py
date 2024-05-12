import dataclasses
from typing import Optional
from src.dto.title.title import TitleDTO, TitleUpdateDTO
from src.dto.base import DTO


@dataclasses.dataclass
class UserRateDTO(DTO):
    id: int
    user_id: int
    title: TitleDTO
    episodes: int
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "UserRateDTO":
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            title=TitleDTO.from_dict(data.get("title")),
            episodes=data.get("episodes"),
            target_id=data.get("target_id"),
            target_type=data.get("target_type"),
            score=data.get("score"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            rewatches=data.get("rewatches"),
            status=data.get("status"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title.to_dict(),
            "status": self.status,
            "episodes": self.episodes,
            "score": self.score,
            "rewatches": self.rewatches,
            "chapters": self.chapters,
            "volumes": self.volumes,
            "target_id": self.target_id,
            "target_type": self.target_type,
        }


@dataclasses.dataclass
class UserRateUpdateDTO(DTO):
    title: TitleUpdateDTO
    episodes: int
    target_id: int
    target_type: str
    score: int
    status: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    rewatches: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "UserRateUpdateDTO":
        return cls(
            title=TitleUpdateDTO.from_dict(data.get("title")),
            episodes=data.get("episodes"),
            target_id=data.get("target_id"),
            target_type=data.get("target_type"),
            score=data.get("score"),
            chapters=data.get("chapters"),
            volumes=data.get("volumes"),
            rewatches=data.get("rewatches"),
            status=data.get("status"),
        )

    def to_dict(self) -> dict:
        return {
            "title": self.title.to_dict(),
            "status": self.status,
            "episodes": self.episodes,
            "score": self.score,
            "rewatches": self.rewatches,
            "chapters": self.chapters,
            "volumes": self.volumes,
            "target_id": self.target_id,
            "target_type": self.target_type,
        }
