from dataclasses import asdict

from shikimori.client import Shikimori

from src.application.dto.user.user import (
    UserRateUpdateDTO,
    UserRateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.user import UserRateEntity


class UpdateUserRateUseCase(UseCase):
    """
    Updating user rate in db and on shikimori
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, obj: UserRateUpdateDTO, token: str) -> UserRateDTO:
        async with self.uow:
            user_rate: UserRateEntity = await self.uow.user_rate.find_one(id=obj.id)

            if not user_rate.is_up_to_date(obj):
                user_rate.update(obj)

                self.shiki.set_token(token)

                await self.shiki.userRate.update(
                    user_rate_id=user_rate.id,
                    episodes=user_rate.episodes,
                    score=user_rate.score,
                    status=user_rate.status,
                    chapters=user_rate.chapters,
                    volumes=user_rate.volumes,
                    rewatches=user_rate.rewatches,
                )

                user_rate = await self.uow.user_rate.edit_one(user_rate)
                await self.uow.commit()

        return UserRateDTO.from_dict(asdict(user_rate))
