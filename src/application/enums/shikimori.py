import enum


class Enum(enum.Enum):
    def __str__(self):
        return self.value


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
