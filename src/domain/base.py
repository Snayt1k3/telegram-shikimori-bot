from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseEntity(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def create(cls, obj) -> "BaseEntity":
        raise NotImplementedError

    @abstractmethod
    def update(self, data) -> "BaseEntity":
        raise NotImplementedError
