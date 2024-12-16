from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase
from src.domain.entities.user_rate import UserRateEntity


class ReadManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by) -> list[UserRateEntity]:
        async with self.uow as uow:
            rates = await uow.user_rate.find_many(**filter_by)

        return rates


class ReadRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by) -> UserRateEntity | None:
        async with self.uow as uow:
            rate = await uow.user_rate.find_one(**filter_by)

        return rate
