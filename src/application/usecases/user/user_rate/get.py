from dataclasses import asdict

from src.application.dto.user.user import (
    UserRateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase, AbstractCache
from src.domain.user import UserEntity


class GetAllUserRates(UseCase):
    """
    Put into cache all user rates from db, and return them
    """

    def __init__(self, uow: AbstractUnitOfWork, cache: AbstractCache):
        self.cache = cache
        self.uow = uow

    async def __call__(self, id_telegram: int) -> list[UserRateDTO]:
        if data := await self.cache.get(f"{id_telegram}_user_rates"):
            return [UserRateDTO.from_dict(asdict(rate)) for rate in data]

        async with self.uow as uow:
            user: UserEntity = await uow.user.find_one(id_telegram=id_telegram)

        rates = [UserRateDTO.from_dict(asdict(rate)) for rate in user.user_rates]

        await self.cache.set(
            f"{id_telegram}_user_rates", [asdict(rate) for rate in rates]
        )

        return rates


class GetUserRate(UseCase):

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def __call__(self, id_telegram: int, id: int) -> UserRateDTO:
        async with self.uow as uow:
            rate = await uow.user_rate.find_one(id_telegram=id_telegram, id=id)

        return UserRateDTO.from_dict(asdict(rate))
