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
            rate: UserRateEntity = await self.uow.user_rate.find_one(id=obj.id)

            if not rate.is_up_to_date(obj):
                rate.update(obj)

                self.shiki.set_token(token)

                await self.shiki.userRate.update(
                    id=rate.user_rate_id,
                    episodes=rate.episodes,
                    score=rate.score,
                    status=rate.status,
                    chapters=rate.chapters,
                    volumes=rate.volumes,
                    rewatches=rate.rewatches,
                )

                user_rate = await self.uow.user_rate.edit_one(rate)
                await self.uow.commit()

        return UserRateDTO.from_dict(asdict(user_rate))