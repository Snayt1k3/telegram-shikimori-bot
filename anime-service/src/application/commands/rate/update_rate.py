from src.application.interfaces import AbstractUow


class UpdateRateCommand:
    """
    Обновляет объект в модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class UpdateManyRateCommand:
    """
    Обновляет объекты в модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
