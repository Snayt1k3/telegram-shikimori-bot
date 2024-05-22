from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.database.sql.title.repo import TitleRepository
from src.adapters.database.sql.notifications.repo import NotificationsRepository
from src.adapters.database.sql.user.repo import UserRepository, UserRateRepository
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.database.sql.base import AbstractRepository

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    title: AbstractRepository
    notifications: AbstractRepository
    user_rate: AbstractRepository
    user: AbstractRepository

    def __init__(self, session_factory):
        self.session_factory = session_factory()

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = await self.session_factory().__aenter__()
        self.title = TitleRepository(self.session)
        self.notifications = NotificationsRepository(self.session)
        self.user_rate = UserRateRepository(self.session)
        self.user = UserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.__aexit__(*args)
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def _commit(self):
        await self.session.commit()
