from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class BaseEntity(metaclass=ABCMeta):
    """
    Base entity class
    """
    pass
