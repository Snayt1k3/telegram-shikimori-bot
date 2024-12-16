from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class UpdateManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, objs: list[dict]) -> None:
        async with self.uow as uow:
            for obj in objs:
                await uow.user_rate.update_one(obj["id"], **obj)


class UpdateRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, id: int, **kwargs):
        async with self.uow as uow:
            await uow.user_rate.update_one(id, **kwargs)
