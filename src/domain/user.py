from dataclasses import dataclass
from typing import Optional

from src.domain.base import BaseEntity
from src.dto.user.user import UserUpdateDTO, UserCreateDTO


@dataclass
class UserEntity(BaseEntity[UserCreateDTO, UserUpdateDTO]):
    id: Optional[str]
    id_telegram: Optional[int]


    @classmethod
    def create(cls, obj: UserCreateDTO) -> "UserEntity":
        pass

    def update(self, data: UserUpdateDTO) -> "UserEntity":
        pass
