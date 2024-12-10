from src.application.interfaces import AbstractUow


class UpdateTitleCommand:
    """
    Обновляет объект в модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class UpdateManyTitleCommand:
    """
    Обновляет объекты в модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
