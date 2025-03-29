from src.adapters.storage.models.user_rate import UserRateModel
from src.application.interfaces import AbstractUow, UseCase
from src.application.dto import RatesGet


class ReadManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: RatesGet) -> list[UserRateModel]:
        async with self.uow as uow:
            rates = await uow.user_rate.find_many(
                **{k: v for k, v in data if v is not None}
            )

        return rates
