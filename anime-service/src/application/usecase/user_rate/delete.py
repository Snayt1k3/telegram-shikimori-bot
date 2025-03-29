from shikimori import Shikimori

from src.application.dto import RateDelete
from src.application.interfaces import AbstractUow, UseCase
from src.tasks.sync import start_delete_rate


class DeleteRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RateDelete) -> int:
        async with self.uow as uow:
            id = await uow.user_rate.delete_one(obj_id=data["id"])

        start_delete_rate(data["id"])

        return id
