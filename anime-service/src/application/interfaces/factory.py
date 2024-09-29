from abc import ABC, abstractmethod
from typing import Awaitable, Callable


class UseCaseFactoryAbstract(ABC):
    """
    Creating usecase and inject deps into him
    """

    @abstractmethod
    def create(self, *args, **kwargs) -> Callable | Awaitable:
        raise NotImplementedError
