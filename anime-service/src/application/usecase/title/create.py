from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class CreateManyTitles(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, objs: list[dict]) -> list[int]:
        async with self.uow as uow:
            title_ids = await uow.title.add_many(objs)
            return title_ids


class CreateTitle(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(
        self,
        id: int,
        title_ru: str,
        title_en: str,
        image_url: str,
        status: str,
        score: int,
        episodes: int,
        episodes_aired: int,
        volumes: int,
        chapters: int,
    ) -> int:
        async with self.uow as uow:
            title_id = await uow.title.add_one(
                id=id,
                title_ru=title_ru,
                title_en=title_en,
                image_url=image_url,
                status=status,
                score=score,
                episodes=episodes,
                episodes_aired=episodes_aired,
                volumes=volumes,
                chapters=chapters,
            )
            return title_id
