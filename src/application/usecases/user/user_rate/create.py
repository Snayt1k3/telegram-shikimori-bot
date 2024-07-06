from dataclasses import asdict

from shikimori.client import Shikimori

from src.application.dto.user.user import (
    UserRateDTO,
    UserCreateDTO,
)
from src.application.interfaces import AbstractUnitOfWork, UseCase
from src.domain.title import TitleEntity
from src.domain.user import UserRateEntity


class CreateUserRateUseCase(UseCase):
    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def _get_title(self, target_type: str, id: int):
        if target_type == "Manga":
            title = await self.shiki.manga.ById(id)
        else:
            title = await self.shiki.anime.ById(id)

        return title

    async def __call__(
        self, id_telegram: int, token: str, obj: UserCreateDTO
    ) -> UserRateDTO:
        async with self.uow as uow:
            user = await uow.user.find_one(id_telegram=id_telegram)
            self.shiki.set_token(token)  # set token for access protected resources

            user_rate = await self.shiki.userRate.create(
                user_id=user.shiki_id,
                target_id=obj.target_id,
                target_type=obj.target_type,
                status=obj.status,
            )
            # check title exists
            title = await uow.title.find_one(target_id=obj.target_id)

            if not title:  # add title to db
                title = await self._get_title(obj.target_type, obj.target_id)
                title = await uow.title.add_one(
                    TitleEntity.create(
                        id=obj.target_id,
                        title_en=title.name,
                        title_ru=title.russian,
                        image_url=title.image.original,
                        status=title.status,
                        score=title.score,
                        episodes=getattr(title, "episodes", None),
                        chapters=getattr(title, "chapters", None),
                        volumes=getattr(title, "volumes", None),
                        episodes_aired=getattr(title, "episodes_aired", None),
                    )
                )

            user_rate = await uow.user_rate.add_one(
                UserRateEntity.create(
                    id=user_rate.id,
                    user=user,
                    title=title,
                    target_id=user_rate.target_id,
                    target_type=user_rate.target_type,
                    status=user_rate.status,
                    score=user_rate.score,
                    episodes=title.episodes,
                    chapters=title.chapters,
                    volumes=title.volumes,
                    rewatches=title.rewatches,
                )
            )

            await uow.commit()
        return UserRateDTO.from_dict(asdict(user_rate))
