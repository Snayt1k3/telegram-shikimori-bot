from typing import TypedDict, Literal


class RatesGet(TypedDict):
    status: (
        Literal["completed", "planned", "rewatching", "dropped", "watching", "on_hold"]
        | None
    )
    user_id: int | None
    ids: list[int] | None


class RatesCreate(TypedDict):
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    shikimori_id: int
    title_id: int
    target_type: Literal["Anime", "Manga"]
    user_id: int


class RatesUpdate(TypedDict):
    id: int
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ]
    score: int | None
    episode: int | None
    volumes: int | None
    rewatches: int | None
    chapters: int | None


class RateDelete(TypedDict):
    id: int
