from shikimori import Shikimori

from src.adapters.storage.models.title import TitleModel
from src.application.dto import TitlesGET
from src.application.interfaces import AbstractUow, UseCase


class ReadManyTitles(UseCase):
    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, data: TitlesGET) -> list[TitleModel]:
        # async with self.uow as uow:
        #     return await uow.title.find_many(**filter_by)
        # todo
        pass


class SearchTitles(UseCase):
    def __init__(self, shiki: Shikimori):
        self.shiki = shiki

    async def __call__(self, data: TitlesGET) -> list[TitleModel]:
        # async with self.uow as uow:
        #     return await uow.title.find_many(**filter_by)
        # todo
        pass
