from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.database.sql.title.repo import TitleRepository
from src.adapters.database.sql.notifications.repo import NotificationsRepository
from src.adapters.database.sql.user.repo import UserRepository, UserRateRepository, ShikiCredsRepository
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.database.sql.repo import AbstractRepository
from src.adapters.database.sql.user.mapper import UserMapper, UserRateMapper, CredsMapper
from src.adapters.database.sql.title.mapper import TitleMapper
from src.adapters.database.sql.notifications.mapper import Notification

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    title: AbstractRepository
    notifications: AbstractRepository
    user_rate: AbstractRepository
    user: AbstractRepository
    shiki_creds: AbstractRepository

    def __init__(self, session_factory):
        self.session_factory = session_factory()

    async def __aenter__(self) -> AbstractUnitOfWork:
        self.session: AsyncSession = await self.session_factory().__aenter__()
        self.title = TitleRepository(self.session, TitleMapper())
        self.notifications = NotificationsRepository(self.session, Notification())
        self.user_rate = UserRateRepository(self.session, UserRateMapper())
        self.user = UserRepository(self.session, UserMapper())
        self.shiki_creds = ShikiCredsRepository(self.session, CredsMapper())
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.__aexit__(*args)
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def _commit(self):
        await self.session.commit()
