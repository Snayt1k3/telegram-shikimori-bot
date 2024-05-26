import asyncio

from shikimori.client import Shikimori
from shikimori.types.user_rates import UserRate

from src.application.dto.user.user import (
    UserRateUpdateDTO,
    UserRateDTO,
)
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.usecases.base import UseCase
from src.domain.title import TitleEntity
from src.domain.user import UserEntity, UserRateEntity


class UpdateUserRatesUseCase(UseCase):
    """Updating all user rates or if user rate does not exist, they will add to db"""

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def _create_title(self, rate: UserRate) -> TitleEntity:

        if rate.target_type == "Anime":
            await asyncio.sleep(0.5)
            title = await self.shiki.anime.ById(rate.target_id)
            data = {"episodes": title.episodes, "episodes_aired": title.episodes_aired}
        else:
            await asyncio.sleep(0.5)
            title = await self.shiki.manga.ById(rate.target_id)
            data = {"chapters": title.chapters, "volumes": title.volumes}

        title = await self.uow.title.add_one(
            {
                "target_id": title.id,
                "title_ru": title.russian,
                "title_en": title.english,
                "image_url": title.image.original_url,
                "status": title.status,
                "score": title.score,
            }
            | data
        )
        return await self.uow.title.find_one(id=title)

    async def _update_user_rate(self, rate: UserRate) -> None:
        user_rate: UserRateEntity = await self.uow.user_rate.find_one(
            target_id=rate.target_id
        )

        new = UserRateUpdateDTO(
            id=user_rate.id,
            episodes=rate.episodes,
            score=rate.score,
            status=rate.status,
            chapters=rate.chapters,
            volumes=rate.volumes,
            rewatches=rate.rewatches,
        )

        if user_rate.is_up_to_date(new):  # check, we don't want to send extra request
            return

        user_rate.update(new)

        await self.shiki.userRate.update(
            id=user_rate.user_rate_id,
            episodes=rate.episodes,
            score=rate.score,
            status=rate.status,
            chapters=rate.chapters,
            volumes=rate.volumes,
            rewatches=rate.rewatches,
        )

    async def __call__(self, id_telegram: int, token: str):
        async with self.uow:
            user: UserEntity = await self.uow.user.find_one(id_telegram=id_telegram)

        self.shiki.set_token(token)

        rates_list: list[UserRate] = []
        rates = await self.shiki.userRate.list(user_id=user.shiki_id, limit=1000)

        rates_list += rates
        page = 0

        while len(rates) == 1000:
            page += 1
            rates = await self.shiki.userRate.list(page=page, limit=1000)
            rates_list += rates

        async with self.uow:

            for rate in rates_list:
                if not user.check_exists_user_rate(rate.target_id, rate.target_type):

                    title_db = await self.uow.title.find_one(target_id=rate.target_id)

                    if not title_db:
                        title_db = await self._create_title(rate)

                    await self.uow.user_rate.add_one(
                        {
                            "user_id": user.id,
                            "title_id": title_db.id,
                            "target_id": rate.target_id,
                            "target_type": rate.target_type,
                            "score": rate.score,
                            "status": rate.status,
                            "episodes": rate.episodes,
                            "volumes": rate.volumes,
                            "chapters": rate.chapters,
                            "rewatches": rate.rewatches,
                        }
                    )

                else:
                    await self._update_user_rate(rate)

            await self.uow.commit()


class UpdateUserRateUseCase(UseCase):
    """
    Updating user rate in db and on shikimori
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, obj: UserRateUpdateDTO) -> UserRateDTO:
        async with self.uow:
            rate: UserRateEntity = await self.uow.user_rate.find_one(id=obj.id)

            if not rate.is_up_to_date(obj):
                rate.update(obj)

                await self.uow.user_rate.edit_one(
                    id=rate.id,
                    data={
                        "episodes": obj.episodes,
                        "status": obj.status,
                        "score": obj.score,
                        "chapters": obj.chapters,
                        "volumes": obj.volumes,
                        "rewatches": obj.rewatches,
                    },
                )

                await self.shiki.userRate.update(
                    id=rate.user_rate_id,
                    episodes=rate.episodes,
                    score=rate.score,
                    status=rate.status,
                    chapters=rate.chapters,
                    volumes=rate.volumes,
                    rewatches=rate.rewatches,
                )
                await self.uow.commit()
        return UserRateDTO()


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

            await self.shiki.userRate.delete(rate.user_rate_id)
            await self.uow.user_rate.delete_one(id)
            await self.uow.commit()
