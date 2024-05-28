from dataclasses import dataclass

@dataclass
class FollowDTO:
    id: int
    en: str
    ru: str
    status: str


@dataclass
class FollowListDTO:
    """
    Class represents  user follow list, which contains title and some info about them
    """

    follows: list[FollowDTO]
