import dataclasses


@dataclasses.dataclass
class TorrentDTO:
    url: str
    episodes: str
    quality: str
    size: int

    @classmethod
    def from_dict(cls, data: dict) -> "TorrentDTO":
        return cls(
            url=data.get("url"),
            episodes=data.get("episodes"),
            quality=data.get("quality"),
            size=data.get("size"),
        )
