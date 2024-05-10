from src.dto.base import DTO


class UserDTO(DTO):

    @classmethod
    def from_dict(cls, data: dict) -> "DTO":
        pass

    def to_dict(self) -> dict:
        pass

class UserUpdateDTO(DTO):
    @classmethod
    def from_dict(cls, data: dict) -> "DTO":
        pass

    def to_dict(self) -> dict:
        pass


class UserCreateDTO(DTO):
    @classmethod
    def from_dict(cls, data: dict) -> "DTO":
        pass

    def to_dict(self) -> dict:
        pass