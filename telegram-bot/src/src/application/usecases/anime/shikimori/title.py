from dataclasses import asdict

from shikimori import Shikimori

from src.application.dto import TitleDTO
from src.application.interfaces import AbstractCache, UseCase, AbstractUnitOfWork
from src.domain.title import TitleEntity


class ShikimoriGetAnimeUseCase(UseCase):
    """
    getting Anime via shikimori api
    """

    def __init__(self, shiki: Shikimori, cache: AbstractCache, uow: AbstractUnitOfWork):
        self.cache = cache
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, id: int) -> TitleDTO:

        if data := await self.cache.get(f"{id}_shikimori"):
            return TitleDTO.from_dict(data)

        async with self.uow as uow:
            title = await uow.title.find_one(id=id)

            if not title:
                title = await self.shiki.anime.ById(id=id)
                title = TitleEntity.create(
                    id=title.id,
                    title_ru=title.russian,
                    title_en=title.name,
                    image_url=title.image.original_url,
                    status=title.status,
                    score=title.score,
                    episodes=title.episodes,
                    episodes_aired=title.episodes_aired,
                    volumes=0,
                    chapters=0,
                )
                await uow.title.add_one(title)
                await uow.commit()

        res = TitleDTO.from_dict(asdict(title))

        await self.cache.set(f"{id}_shikimori", asdict(res), expire_in=60 * 60 * 24)

        return res
