from typing import TypedDict, Literal


class RatesGet(TypedDict):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    user_id: int
    ids: str


class RatesCreate(TypedDict):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    title_id: int


class RatesUpdate(TypedDict):
    id: int
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    score: int
    episode: int
    volumes: int
    rewatches: int
    chapters: int


class RateDelete(TypedDict):
    id: int
