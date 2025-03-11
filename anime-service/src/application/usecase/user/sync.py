from shikimori import Shikimori

from src.application.dto import JobStatus
from src.application.interfaces import AbstractUow, UseCase


class SyncUserRates(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, user_id: int) -> JobStatus:
        raise NotImplementedError


class SyncUserRate(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, rate_id: int) -> JobStatus:
        raise NotImplementedError
