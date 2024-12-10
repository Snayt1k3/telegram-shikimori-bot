from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class DeleteManyTitles(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, ids: list[int]) -> list[int]:
        async with self.uow as uow:
            return await uow.title.delete_many(ids)


class DeleteTitle(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, id: int) -> int | None:
        async with self.uow as uow:
            return await uow.title.delete_one(id)
