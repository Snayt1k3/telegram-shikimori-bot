from src.application.dto import RatesUpdate
from src.application.interfaces import AbstractUow, UseCase


class UpdateRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RatesUpdate):
        # async with self.uow as uow:
        #     await uow.user_rate.update_one(id, **kwargs) todo
        pass
