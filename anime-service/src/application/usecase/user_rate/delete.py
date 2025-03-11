from src.application.interfaces import AbstractUow, UseCase
from src.application.dto import RateDelete


class DeleteRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RateDelete):
        async with self.uow as uow:
            await uow.user_rate.delete_one(obj_id=data["id"])
