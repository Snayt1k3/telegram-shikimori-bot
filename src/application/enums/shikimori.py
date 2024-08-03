from .base import Enum


class ShikimoriListType(Enum):
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLANNED = "planned"
    REWATCHING = "rewatching"


class ShikimoriEntryType(Enum):
    ANIME = "Anime"
    MANGA = "Manga"
