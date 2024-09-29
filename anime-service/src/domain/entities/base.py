import dataclasses
from abc import ABC, abstractmethod


@dataclasses.dataclass
class Entity(ABC):
    id: int

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "Entity":
        raise NotImplementedError
