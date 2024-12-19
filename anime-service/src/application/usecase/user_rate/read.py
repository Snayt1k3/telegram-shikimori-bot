from src.adapters.storage.models.user_rate import UserRateModel
from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class ReadManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by) -> list[UserRateModel]:
        async with self.uow as uow:
            rates = await uow.user_rate.find_many(**filter_by)

        return rates


class ReadRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by) -> UserRateModel | None:
        async with self.uow as uow:
            rate = await uow.user_rate.find_one(**filter_by)

        return rate
