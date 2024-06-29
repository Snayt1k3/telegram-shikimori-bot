from contextlib import asynccontextmanager
from typing import AsyncIterator, AsyncContextManager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.adapters.anilibria import anilibria_client
from src.adapters.shiki import shiki_client
from src.adapters.cache import RedisCache
from src.adapters.common.config import RedisCfg
from src.adapters.database.uow.uow import SqlAlchemyUnitOfWork
from src.application.usecases.anime import (
    AnilibriaSearchUseCase,
    GetTorrentUseCase,
    ShikimoriSearchUseCase,
    GetUserListUseCase,
)
from src.application.usecases.user import (
    AddUserUseCase,
    DeleteUserUseCase,
    AddFollowUseCase,
    DeleteFollowUseCase,
    GetAllFollowsUseCase,
    CreateUserRateUseCase,
    DeleteUserRateUseCase,
    GetAllUserRates,
    UpdateUserRateUseCase,
    GetCredentialsUseCase,
    GetURIUseCase,
    SynchronizeUserRate,
    GetUserRate,
)
from src.presentation.telegram.interactor_factory import InteractorFactory


class IoC(InteractorFactory):
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def add_user(self) -> AsyncIterator[AddUserUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield AddUserUseCase(shiki_client, uow)

    @asynccontextmanager
    async def add_follow(self) -> AsyncIterator[AddFollowUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield AddFollowUseCase(uow)

    @asynccontextmanager
    async def delete_user(self) -> AsyncIterator[DeleteUserUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield DeleteUserUseCase(uow)

    @asynccontextmanager
    async def remove_follow(self) -> AsyncIterator[DeleteFollowUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield DeleteFollowUseCase(uow)

    @asynccontextmanager
    async def all_follows(self) -> AsyncIterator[GetAllFollowsUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        cache = RedisCache(RedisCfg())
        yield GetAllFollowsUseCase(anilibria_client, uow, cache)

    @asynccontextmanager
    async def add_user_rate(self) -> AsyncIterator[CreateUserRateUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield CreateUserRateUseCase(shiki_client, uow)

    @asynccontextmanager
    async def delete_user_rate(self) -> AsyncIterator[DeleteUserRateUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield DeleteUserRateUseCase(shiki_client, uow)

    @asynccontextmanager
    async def get_user_rates(self) -> AsyncIterator[GetAllUserRates]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        cache = RedisCache(RedisCfg())
        yield GetAllUserRates(uow, cache)

    @asynccontextmanager
    async def update_user_rate(self) -> AsyncIterator[UpdateUserRateUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield UpdateUserRateUseCase(shiki_client, uow)

    @asynccontextmanager
    async def get_credentials(self) -> AsyncIterator[GetCredentialsUseCase]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield GetCredentialsUseCase(shiki_client, uow)

    @asynccontextmanager
    async def anilibria_search(self) -> AsyncIterator[AnilibriaSearchUseCase]:
        cache = RedisCache(RedisCfg())
        yield AnilibriaSearchUseCase(anilibria_client, cache)

    @asynccontextmanager
    async def anilibria_get_torrent(self) -> AsyncIterator[GetTorrentUseCase]:
        yield GetTorrentUseCase(anilibria_client)

    @asynccontextmanager
    async def shikimori_search(self) -> AsyncIterator[ShikimoriSearchUseCase]:
        cache = RedisCache(RedisCfg())
        yield ShikimoriSearchUseCase(shiki_client, cache)

    @asynccontextmanager
    async def shikimori_get_list(self) -> AsyncIterator[GetUserListUseCase]:
        cache = RedisCache(RedisCfg())
        uow = SqlAlchemyUnitOfWork(self._session_factory)

        yield GetUserListUseCase(uow, cache)

    @asynccontextmanager
    async def get_shikimori_uri(self) -> AsyncIterator[GetURIUseCase]:
        yield GetURIUseCase(shiki_client)

    @asynccontextmanager
    async def sync_user_rates(self) -> AsyncIterator[SynchronizeUserRate]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield SynchronizeUserRate(shiki_client, uow)

    @asynccontextmanager
    async def get_user_rate(self) -> AsyncContextManager[GetUserRate]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield GetUserRate(uow)
