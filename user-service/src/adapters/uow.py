from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces import AbstractUow
from src.adapters.storage.repository import user_rate, title


class SqlAlchemyUnitOfWork(AbstractUow):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self) -> AbstractUow:
        self.session: AsyncSession = await anext(self.session_factory)
        self.title = title.TitleRepo(self.session)
        self.user_rate = user_rate.UserRateRepo(self.session)
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
