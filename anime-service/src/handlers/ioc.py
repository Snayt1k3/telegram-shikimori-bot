from contextlib import asynccontextmanager
from typing import AsyncIterator

from shikimori import Shikimori

from src.adapters.uow import SqlAlchemyUnitOfWork
from src.application import usecase
from src.config.shiki import shiki_cfg


class IoC:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @property
    def _shiki(self) -> Shikimori:
        return Shikimori(
            user_agent=shiki_cfg.SHIKI_UA,
            client_id=shiki_cfg.SHIKI_CLIENT_ID,
            client_secret=shiki_cfg.SHIKI_CLIENT_SECRET,
            raise_on_error=True,
        )

    @property
    def _uow(self) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self.session_factory)

    @asynccontextmanager
    async def read_titles(self) -> AsyncIterator[usecase.ReadManyTitles]:
        yield usecase.ReadManyTitles(self._uow)

    @asynccontextmanager
    async def update_rate(self) -> AsyncIterator[usecase.UpdateRate]:
        yield usecase.UpdateRate(self._uow)

    @asynccontextmanager
    async def delete_rate(self) -> AsyncIterator[usecase.DeleteRate]:
        yield usecase.DeleteRate(self._shiki, self._uow)

    @asynccontextmanager
    async def read_rates(self) -> AsyncIterator[usecase.ReadManyRates]:
        yield usecase.ReadManyRates(self._uow)

    @asynccontextmanager
    async def add_rate(self) -> AsyncIterator[usecase.CreateRate]:
        yield usecase.CreateRate(self._uow, self._shiki)

    @asynccontextmanager
    async def sync_rate(self) -> AsyncIterator[usecase.SyncUserRateTask]:
        yield usecase.SyncUserRateTask(self._uow, self._shiki)

    @asynccontextmanager
    async def load_rates(self) -> AsyncIterator[usecase.LoadAllUserRates]:
        yield usecase.LoadAllUserRates(self._uow, self._shiki)

    @asynccontextmanager
    async def get_profile(self) -> AsyncIterator[usecase.UserProfile]:
        yield usecase.UserProfile(self._uow, self._shiki)

    @asynccontextmanager
    async def mal_load(self) -> AsyncIterator[usecase.MalLoad]:
        yield usecase.MalLoad(self._uow)

    @asynccontextmanager
    async def shikimori_load_animes(self) -> AsyncIterator[usecase.ShikimoriLoadAnimes]:
        yield usecase.ShikimoriLoadAnimes(self._uow, self._shiki)

    @asynccontextmanager
    async def shikimori_load_mangas(self) -> AsyncIterator[usecase.ShikimoriLoadMangas]:
        yield usecase.ShikimoriLoadMangas(self._uow, self._shiki)
