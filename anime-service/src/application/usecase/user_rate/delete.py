from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class DeleteManyRates(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class DeleteRate(UseCase):

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
