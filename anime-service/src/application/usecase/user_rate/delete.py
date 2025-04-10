from shikimori import Shikimori

from src.application.dto import RateDelete
from src.application.interfaces import AbstractUow, UseCase


class DeleteRate(UseCase):

    def __init__(self, shiki: Shikimori, uow: AbstractUow):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: RateDelete) -> int:
        async with self.uow as uow:
            id = await uow.user_rate.delete_one(obj_id=data["id"])
            await self.shiki.userRate.delete(id=data["id"])

        return id
