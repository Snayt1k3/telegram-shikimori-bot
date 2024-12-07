from abc import ABC, abstractmethod

from src.application.interfaces.usecase import UseCase


class UseCaseFactoryAbstract(ABC):
    """
    Creating usecase and inject deps into him
    """

    @abstractmethod
    def create(self, *args, **kwargs) -> UseCase:
        raise NotImplementedError
