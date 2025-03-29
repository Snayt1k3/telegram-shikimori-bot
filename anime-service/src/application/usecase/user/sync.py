from shikimori import Shikimori
from shikimori.exceptions import RequestError

from src.adapters.storage.models.user_rate import UserRateModel
from src.application.dto import JobStatus
from src.application.interfaces import AbstractUow, UseCase


class SyncUserRatesTask(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, user_id: int) -> JobStatus:
        # Не забыть - накатить новую миграцию.
        # Логика - UseRate отсутствует в бд, но есть в шикимори, грузим в бд.
        # И если обновление на шикимори было позже грузим его, иначе ничего не делаем.

        raise NotImplementedError


class SyncUserRateTask(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, rate_id: int) -> JobStatus:
        try:

            async with self._uow as uow:
                rate: UserRateModel = await uow.user_rate.find_one(id=rate_id)

            response = await self._shiki.userRate.update(
                user_rate_id=rate.id,
                status=rate.status,
                score=rate.score,
                chapters=rate.chapters,
                volumes=rate.volumes,
                episodes=rate.episodes,
                rewatches=rate.rewatches,
            )

            if isinstance(response, RequestError):
                raise response

            return JobStatus(success=True, error=None)

        except Exception as e:
            return JobStatus(success=False, error=str(e))


class DeleteUserRateTask(UseCase):
    def __init__(self, shiki: Shikimori) -> None:
        self._shiki = shiki

    async def __call__(self, rate_id: int) -> JobStatus:
        try:

            response = await self._shiki.userRate.delete(
                id=rate_id
            )

            if isinstance(response, RequestError):
                raise response

            return JobStatus(success=True, error=None)

        except Exception as e:
            return JobStatus(success=False, error=str(e))
