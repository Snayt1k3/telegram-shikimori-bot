from abc import ABCMeta, abstractmethod
from typing import Optional, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")  # create
U = TypeVar("U")  # update

@dataclass
class BaseEntity(Generic[T, U], metaclass=ABCMeta):
    id: Optional[str | int]

    @classmethod
    @abstractmethod
    def create(cls, obj: T) -> "BaseEntity":
        raise NotImplementedError

    @abstractmethod
    def update(self, data: U) -> "BaseEntity":
        raise NotImplementedError
