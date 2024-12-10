from src.application.interfaces import AbstractUow


class DeleteRateCommand:
    """
    Удаляет объект из модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class DeleteManyRateCommand:
    """
    Удаляет объекты из модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
