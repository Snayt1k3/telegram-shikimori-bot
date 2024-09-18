from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractUow


class SqlAlchemyUnitOfWork(AbstractUow):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self) -> AbstractUow:
        self.session: AsyncSession = self.session_factory()
        self.title = ...
        self.user_rate = ...
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()

        else:
            await self._rollback()

    async def _rollback(self):
        await self.session.rollback()

    async def _commit(self):
        await self.session.commit()
