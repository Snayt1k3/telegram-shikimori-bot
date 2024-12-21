from contextlib import asynccontextmanager
from typing import AsyncContextManager

from src.adapters.uow import SqlAlchemyUnitOfWork
from src.application import usecase


class IoC:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @asynccontextmanager
    async def read_title(self) -> AsyncContextManager[usecase.ReadTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadTitle(uow)

    @asynccontextmanager
    async def read_titles(self) -> AsyncContextManager[usecase.ReadManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyTitles(uow)

    @asynccontextmanager
    async def update_rates(self) -> AsyncContextManager[usecase.UpdateManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateManyRates(uow)

    @asynccontextmanager
    async def update_rate(self) -> AsyncContextManager[usecase.UpdateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateRate(uow)

    @asynccontextmanager
    async def update_title(self) -> AsyncContextManager[usecase.UpdateTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateTitle(uow)

    @asynccontextmanager
    async def update_titles(self) -> AsyncContextManager[usecase.UpdateManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateManyTitles(uow)

    @asynccontextmanager
    async def delete_title(self) -> AsyncContextManager[usecase.DeleteTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteTitle(uow)

    @asynccontextmanager
    async def delete_titles(self) -> AsyncContextManager[usecase.DeleteManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteManyTitles(uow)

    @asynccontextmanager
    async def delete_rate(self) -> AsyncContextManager[usecase.DeleteRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteRate(uow)

    @asynccontextmanager
    async def delete_rates(self) -> AsyncContextManager[usecase.DeleteManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteManyRates(uow)

    @asynccontextmanager
    async def read_rate(self) -> AsyncContextManager[usecase.ReadRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadRate(uow)

    @asynccontextmanager
    async def read_rates(self) -> AsyncContextManager[usecase.ReadManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyRates(uow)

    @asynccontextmanager
    async def add_title(self) -> AsyncContextManager[usecase.CreateTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateTitle(uow)

    @asynccontextmanager
    async def add_titles(self) -> AsyncContextManager[usecase.CreateManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateManyTitles(uow)

    @asynccontextmanager
    async def add_rate(self) -> AsyncContextManager[usecase.CreateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateRate(uow)

    @asynccontextmanager
    async def add_rates(self) -> AsyncContextManager[usecase.CreateManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateManyRates(uow)
