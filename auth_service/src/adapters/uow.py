import abc

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.storage.repo import AbstractRepository, UserRepo


class AbstractUow(abc.ABC):
    user: AbstractRepository

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


class SqlAlchemyUnitOfWork(AbstractUow):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self) -> AbstractUow:
        self.session: AsyncSession = await anext(self.session_factory)
        self.user = UserRepo(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self._rollback()

    async def _rollback(self):
        await self.session.rollback()

    async def _commit(self):
        await self.session.commit()
