import abc
from src.application.interfaces import AbstractRepository


class AbstractUow(abc.ABC):
    title: AbstractRepository
    user_rate: AbstractRepository

    @abc.abstractmethod
    async def __aenter__(self) -> "AbstractUow":
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError
