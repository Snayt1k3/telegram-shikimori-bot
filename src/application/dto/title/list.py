import dataclasses

from src.application.dto.user.user import UserRateDTO
from src.application.enums.shikimori import ShikimoriListType


@dataclasses.dataclass
class UserListDTO:
    """
    obj which represents a shikimori list
    """
    objs: list[UserRateDTO]
    type: ShikimoriListType
    length: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            objs=[UserRateDTO.from_dict(i) for i in data["objs"]],
            type=ShikimoriListType(data.get("type")),
            length=data.get("length"),
        )
