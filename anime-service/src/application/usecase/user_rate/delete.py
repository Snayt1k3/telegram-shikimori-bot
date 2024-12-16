from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class DeleteManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, ids: list[int]):
        async with self.uow as uow:
            await uow.user_rate.delete_many(ids)


class DeleteRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, id: int):
        async with self.uow as uow:
            await uow.user_rate.delete_one(id)
