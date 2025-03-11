from contextlib import asynccontextmanager
from typing import AsyncIterator

from shikimori import Shikimori

from src.adapters.uow import SqlAlchemyUnitOfWork
from src.application import usecase
from src.config.shiki import shiki_cfg


class IoC:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @asynccontextmanager
    async def read_titles(self) -> AsyncIterator[usecase.ReadManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyTitles(uow)

    @asynccontextmanager
    async def update_rate(self) -> AsyncIterator[usecase.UpdateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateRate(uow)

    @asynccontextmanager
    async def delete_rate(self) -> AsyncIterator[usecase.DeleteRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteRate(uow)

    @asynccontextmanager
    async def read_rates(self) -> AsyncIterator[usecase.ReadManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyRates(uow)

    @asynccontextmanager
    async def add_rate(self) -> AsyncIterator[usecase.CreateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateRate(uow)

    @asynccontextmanager
    async def sync_rate(self) -> AsyncIterator[usecase.SyncUserRate]:
        shiki = Shikimori(
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
        )
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.SyncUserRate(uow, shiki)

    @asynccontextmanager
    async def sync_rates(self) -> AsyncIterator[usecase.SyncUserRates]:
        shiki = Shikimori(
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
        )
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.SyncUserRates(uow, shiki)

    @asynccontextmanager
    async def load_rates(self) -> AsyncIterator[usecase.LoadAllUserRates]:
        shiki = Shikimori(
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
        )
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.LoadAllUserRates(uow, shiki)

    @asynccontextmanager
    async def get_profile(self) -> AsyncIterator[usecase.UserProfile]:
        shiki = Shikimori(
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
        )
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UserProfile(uow, shiki)
