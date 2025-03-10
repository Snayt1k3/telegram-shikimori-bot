from shikimori import Shikimori

from src.application.dto.job import JobStatus
from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


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
