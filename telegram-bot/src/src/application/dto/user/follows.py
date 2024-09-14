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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(follows=[FollowDTO(**f) for f in data.get("follows")])
