import dataclasses


@dataclasses.dataclass
class Torrent:
    url: str
    episodes: str
    quality: str
    size: int
