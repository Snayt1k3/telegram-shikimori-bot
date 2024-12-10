from src.application.interfaces import AbstractUow


class CreateTitleCommand:
    """
    Создает объект в модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class CreateManyTitleCommand:
    """
    Создает объекты в модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
