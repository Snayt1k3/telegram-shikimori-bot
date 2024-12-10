from src.application.interfaces import AbstractUow


class DeleteTitleCommand:
    """
    Удаляет объект из модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class DeleteManyTitleCommand:
    """
    Удаляет объекты из модели "Title".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
