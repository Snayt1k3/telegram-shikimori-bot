from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase
from src.domain.entities.title import TitleEntity


class ReadManyTitles(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by: dict) -> list[TitleEntity]:
        async with self.uow as uow:
            return await uow.title.find_many(**filter_by)


class ReadTitle(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, **filter_by: dict) -> TitleEntity | None:
        async with self.uow as uow:
            return await uow.title.find_one(**filter_by)
