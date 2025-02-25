from typing import Literal

from src.dto.base import Model


class RateUpdateDTO(Model):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    score: int = None
    episode: int = None
    volumes: int = None
    rewatches: int = None
    chapters: int = None


class RateAddDTO(Model):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    title_id: int


class RateFilterDTO(Model):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None
    user_id: int = None
    ids: list[int] = None
