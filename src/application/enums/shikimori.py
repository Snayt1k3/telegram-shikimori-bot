import enum


class ShikimoriListType(enum.Enum):
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLANNED = "planned"
    REWATCHING = "rewatching"

    def __str__(self):
        return self.value
