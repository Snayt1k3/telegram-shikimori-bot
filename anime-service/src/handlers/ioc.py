from contextlib import asynccontextmanager
from typing import  AsyncIterator

from src.adapters.uow import SqlAlchemyUnitOfWork
from src.application import usecase


class IoC:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @asynccontextmanager
    async def read_title(self) -> AsyncIterator[usecase.ReadTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadTitle(uow)

    @asynccontextmanager
    async def read_titles(self) -> AsyncIterator[usecase.ReadManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyTitles(uow)

    @asynccontextmanager
    async def update_rates(self) -> AsyncIterator[usecase.UpdateManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateManyRates(uow)

    @asynccontextmanager
    async def update_rate(self) -> AsyncIterator[usecase.UpdateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateRate(uow)

    @asynccontextmanager
    async def update_title(self) -> AsyncIterator[usecase.UpdateTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateTitle(uow)

    @asynccontextmanager
    async def update_titles(self) -> AsyncIterator[usecase.UpdateManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.UpdateManyTitles(uow)

    @asynccontextmanager
    async def delete_title(self) -> AsyncIterator[usecase.DeleteTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteTitle(uow)

    @asynccontextmanager
    async def delete_titles(self) -> AsyncIterator[usecase.DeleteManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteManyTitles(uow)

    @asynccontextmanager
    async def delete_rate(self) -> AsyncIterator[usecase.DeleteRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteRate(uow)

    @asynccontextmanager
    async def delete_rates(self) -> AsyncIterator[usecase.DeleteManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.DeleteManyRates(uow)

    @asynccontextmanager
    async def read_rate(self) -> AsyncIterator[usecase.ReadRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadRate(uow)

    @asynccontextmanager
    async def read_rates(self) -> AsyncIterator[usecase.ReadManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.ReadManyRates(uow)

    @asynccontextmanager
    async def add_title(self) -> AsyncIterator[usecase.CreateTitle]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateTitle(uow)

    @asynccontextmanager
    async def add_titles(self) -> AsyncIterator[usecase.CreateManyTitles]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateManyTitles(uow)

    @asynccontextmanager
    async def add_rate(self) -> AsyncIterator[usecase.CreateRate]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateRate(uow)

    @asynccontextmanager
    async def add_rates(self) -> AsyncIterator[usecase.CreateManyRates]:
        uow = SqlAlchemyUnitOfWork(self.session_factory)
        yield usecase.CreateManyRates(uow)
