from shikimori.client import Shikimori

from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.user import UserRateEntity


class DeleteUserRateUseCase(UseCase):
    """
    delete user_rate from db and shikimori
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, id: int):
        async with self.uow:
            rate: UserRateEntity = await self.uow.user_rate.find_one(id=id)

            await self.shiki.userRate.delete(rate.id)
            await self.uow.user_rate.delete_one(id)
            await self.uow.commit()
