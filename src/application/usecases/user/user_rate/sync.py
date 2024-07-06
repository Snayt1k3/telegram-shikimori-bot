import asyncio
from dataclasses import asdict

from shikimori.client import Shikimori
from shikimori.types.user_rates import UserRate

from src.application.dto.user.user import (
    UserRateUpdateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.title import TitleEntity
from src.domain.user import UserEntity, UserRateEntity
from src.application.common import retry


class SynchronizeUserRate(UseCase):
    """
    Getting all user rates from shikimori and synchronize db with them
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.uow = uow
        self.shiki = shiki

    @retry.retry(exp_size=2)
    async def _create_title(self, rate: UserRate) -> TitleEntity:

        title = await self.uow.title.find_one(target_id=rate.target_id)

        if title:
            return title

        await asyncio.sleep(0.2)
        if rate.target_type == "Anime":
            title = await self.shiki.anime.ById(rate.target_id)
        else:
            title = await self.shiki.manga.ById(rate.target_id)

        title_id = await self.uow.title.add_one(
            TitleEntity.create(
                id=title.id,
                title_en=title.name,
                title_ru=title.russian,
                image_url=title.image.original_url,
                status=title.status,
                score=title.score,
                episodes=getattr(title, "episodes", None),
                chapters=getattr(title, "chapters", None),
                volumes=getattr(title, "volumes", None),
                episodes_aired=getattr(title, "episodes_aired", None),
            )
        )

        title = await self.uow.title.find_one(id=title_id)
        return title

    async def _get_all_user_rates(self, shiki_id: int) -> list[UserRate]:
        rates_list: list[UserRate] = []
        rates = await self.shiki.userRate.list(user_id=shiki_id, limit=1000)

        rates_list += rates
        page = 0

        while len(rates) == 1000:
            page += 1
            rates = await self.shiki.userRate.list(page=page, limit=1000)
            rates_list += rates

        return rates

    async def __call__(self, id_telegram: int, token: str) -> None:
        async with self.uow:
            user: UserEntity = await self.uow.user.find_one(id_telegram=id_telegram)
            self.shiki.set_token(token)
            rates = await self._get_all_user_rates(user.shiki_id)

            for rate in rates:
                new = UserRateUpdateDTO.from_dict(asdict(rate))
                title = await self._create_title(rate)

                if user.check_exists_user_rate(rate.target_id, rate.target_type):
                    rate_db = await self.uow.user_rate.find_one(
                        target_id=rate.target_id
                    )
                    rate_db.update(new)

                    await self.uow.user_rate.edit_one(rate_db)
                else:
                    await self.uow.user_rate.add_one(
                        UserRateEntity.create(
                            id=rate.id,
                            user=user,
                            title=title,
                            target_id=rate.target_id,
                            target_type=rate.target_type,
                            status=rate.status,
                            score=rate.score,
                            episodes=rate.episodes,
                            chapters=rate.chapters,
                            volumes=rate.volumes,
                            rewatches=rate.rewatches,
                        )
                    )
            await self.uow.commit()
