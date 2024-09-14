import dataclasses
import datetime


@dataclasses.dataclass
class ShikiCredsDTO:
    id: int
    access: str
    refresh: str
    expire_in: datetime.datetime

    @classmethod
    def from_dict(cls, data: dict) -> "ShikiCredsDTO":
        return cls(
            id=data["id"],
            access=data["access"],
            refresh=data["refresh"],
            expire_in=datetime.datetime.fromtimestamp(data["expire_in"]),
        )


@dataclasses.dataclass
class ShikiCredsCreateDTO:
    access: str
    refresh: str
    expire_in: datetime.datetime

    @classmethod
    def from_dict(cls, data: dict) -> "ShikiCredsCreateDTO":
        return cls(
            access=data["access"],
            refresh=data["refresh"],
            expire_in=datetime.datetime.fromtimestamp(data["expire_in"]),
        )

@dataclasses.dataclass
class ShikiCredsUpdateDTO:
    access: str
    refresh: str
    expire_in: datetime.datetime

    @classmethod
    def from_dict(cls, data: dict) -> "ShikiCredsUpdateDTO":
        return cls(
            access=data["access"],
            refresh=data["refresh"],
            expire_in=datetime.datetime.fromtimestamp(data["expire_in"]),
        )