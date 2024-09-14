from __future__ import annotations

import abc

from src.application.interfaces.database.repo import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    title: AbstractRepository
    notifications: AbstractRepository
    user_rate: AbstractRepository
    user: AbstractRepository
    shiki_creds: AbstractRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._commit()

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError
