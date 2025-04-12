from shikimori import Shikimori

from src.application.dto import RatesCreate
from src.application.interfaces import AbstractUow, UseCase


class CreateRate(UseCase):

    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self.uow = uow
        self.shiki = shiki

    async def __call__(self, data: RatesCreate) -> int:
        response = await self.shiki.userRate.create(
            user_id=data["user_id"],
            target_id=data["title_id"],
            target_type=data["target_type"],
            status=data["status"],
        )

        async with self.uow as uow:
            obj_id = await uow.user_rate.add_one(
                id=response.id,
                status=data["status"],
                target_id=data["title_id"],
                target_type=data["target_type"],
                shikimori_id=data["shikimori_id"],
                user_id=data["user_id"],
            )

        return obj_id
