from shikimori import Shikimori

from src.adapters.storage.models.user_rate import UserRateModel
from src.application.dto import JobStatus
from src.application.interfaces import AbstractUow, UseCase


class SyncUserRateTask(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, rate_id: int) -> JobStatus:
        async with self._uow as uow:
            rate: UserRateModel = await uow.user_rate.find_one(id=rate_id)

        await self._shiki.userRate.update(
            user_rate_id=rate.id,
            status=rate.status,
            score=rate.score,
            chapters=rate.chapters,
            volumes=rate.volumes,
            episodes=rate.episodes,
            rewatches=rate.rewatches,
        )

        return JobStatus(success=True, error=None)


class DeleteUserRateTask(UseCase):
    def __init__(self, shiki: Shikimori) -> None:
        self._shiki = shiki

    async def __call__(self, rate_id: int) -> JobStatus:
        await self._shiki.userRate.delete(id=rate_id)
        return JobStatus(success=True, error=None)
