from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.database.uow.base import AbstractUnitOfWork

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        super().__init__()
        # todo добавить репозитории
        self.session_factory = session_factory()

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = await self.session_factory().__aenter__()
        # todo добавить репозитории
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.__aexit__(*args)
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def _commit(self):
        await self.session.commit()
