import asyncio
from dataclasses import asdict

from shikimori.client import Shikimori
from shikimori.types.user_rates import UserRate

from src.application.dto.user.user import (
    UserRateUpdateDTO,
    UserRateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.title import TitleEntity
from src.domain.user import UserEntity, UserRateEntity


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

                user_rate = await self.uow.user_rate.edit_one(
                    id=rate.id, data=asdict(obj)
                )
                await self.uow.commit()

        return UserRateDTO.from_dict(asdict(user_rate))


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


class GetAllUserRates(UseCase):
    """
    Put into cache all user rates from db, and return them
    """

    def __init__(self, uow: AbstractUnitOfWork, cache: "AbstractCache"):
        self.cache = cache
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class SynchronizeUserRate(UseCase):
    """
    Getting all user rates from shikimori and synchronize db with them
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.uow = uow
        self.shiki = shiki

    async def _create_title(self, rate: UserRate) -> TitleEntity:

        title = await self.uow.title.find_one(target_id=rate.target_id)

        if title:
            return title

        await asyncio.sleep(0.2)
        if rate.target_type == "Anime":
            title = await self.shiki.anime.ById(rate.target_id)
            data = {"episodes": title.episodes, "episodes_aired": title.episodes_aired}
        else:
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

                    await self.uow.user_rate.edit_one(rate_db.id, asdict(new))
                else:
                    await self.uow.user_rate.add_one(
                        {
                            "user_id": user.id,
                            "title_id": title.id,
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
        await self.uow.commit()
