from typing import Literal
from pydantic import BaseModel


class RateUpdateDTO(BaseModel):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    score: int = None
    episode: int = None
    volumes: int = None
    rewatches: int = None
    chapters: int = None


class RateAddDTO(BaseModel):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    shikimori_id: int
    title_id: int
    target_type: Literal["Anime", "Manga"]
    user_id: int


class RateFilterDTO(BaseModel):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    user_id: int = None
