from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.adapters.clients import shiki_client
from src.adapters.database.uow.uow import SqlAlchemyUnitOfWork
from src.application.usecases.user import AddUserUseCase
from src.presentation.telegram.interactor_factory import InteractorFactory


class IoC(InteractorFactory):
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def add_user(self) -> AsyncIterator["AddUserUseCase"]:
        uow = SqlAlchemyUnitOfWork(self._session_factory)
        yield AddUserUseCase(shiki_client, uow)

