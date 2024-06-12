import enum

class BaseEnum(enum.Enum):
    def __str__(self):
        return self.value


class SearchEngineEnum(BaseEnum):
    shikimori = "Shikimori"
    anilibria = "Anilibria"
