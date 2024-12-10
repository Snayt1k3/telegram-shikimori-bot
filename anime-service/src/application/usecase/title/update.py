from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase
from src.domain.entities.base import Entity


class UpdateTitle(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, id: int, **kwargs) -> Entity:
        async with self.uow as uow:
            return await uow.title.update_one(id=id, **kwargs)
