from abc import ABCMeta, abstractmethod
from typing import Optional
from dataclasses import dataclass


@dataclass
class BaseEntity(metaclass=ABCMeta):
    id: Optional[str | int]

    @classmethod
    @abstractmethod
    def create(cls, obj) -> "BaseEntity":
        raise NotImplementedError

    @abstractmethod
    def update(self, data) -> "BaseEntity":
        raise NotImplementedError
