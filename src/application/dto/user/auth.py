import dataclasses


@dataclasses.dataclass
class ShikiCredsDTO:
    id: int
    access: str
    refresh: str
    expire_in: str

    @classmethod
    def from_dict(cls, data: dict) -> "ShikiCredsDTO":
        return cls(
            id=data["id"],
            access=data["access"],
            refresh=data["refresh"],
            expire_in=data["expire_in"],
        )


@dataclasses.dataclass
class ShikiCredsCreateDTO:
    access: str
    refresh: str
    expire_in: str

    @classmethod
    def from_dict(cls, data: dict) -> "ShikiCredsCreateDTO":
        return cls(
            access=data["access"],
            refresh=data["refresh"],
            expire_in=data["expire_in"],
        )
