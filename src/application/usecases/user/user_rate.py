from shikimori.client import Shikimori
from shikimori.types.user_rates import UserRate

from src.application.dto.user.user import (
    UserDTO,
    UserRateUpdateDTO,
    UserRateDTO,
)
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.usecases.base import UseCase


class GetAllUserRatesUseCase(UseCase):
    """
    getting a current user rates from profile
    """

    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self, token: str) -> UserRate:
        self.shiki.set_token(token)
        rates = await self.shiki.userRate.list(limit=1000)
        return rates


class UpdateUserRatesUseCase(UseCase):
    """Updating all user rates or if user rate does not exist"""

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, id_telegram: int) -> UserDTO:
        pass


class UpdateUserRateUseCase(UseCase):
    """
    Updating user rate in db and on shikimori
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, obj: UserRateUpdateDTO) -> UserRateDTO:
        pass


class DeleteUserRateUseCase(UseCase):
    """
    delete user_rate from db and shikimori
    """

    def __call__(self, id: int):
        pass
