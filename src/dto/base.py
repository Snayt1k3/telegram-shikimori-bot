from abc import abstractmethod, ABC

class DTO(ABC):

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "DTO":
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

