import dataclasses


@dataclasses.dataclass
class ShikiCredsDTO:
    id: int
    access: str
    refresh: str
    expire_in: str


@dataclasses.dataclass
class ShikiCredsCreateDTO:
    access: str
    refresh: str
    expire_in: str
