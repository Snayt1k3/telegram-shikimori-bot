from src.adapters.storage.models.title import TitleModel
from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class UpdateTitle(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, id: int, **kwargs) -> TitleModel:
        async with self.uow as uow:
            return await uow.title.update_one(id=id, **kwargs)


class UpdateManyTitles(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, objs: list[dict]) -> TitleModel:
        pass
