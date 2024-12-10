from src.application.interfaces import AbstractUow


class CreateRateCommand:
    """
    Создает объект в модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass


class CreateManyRateCommand:
    """
    Создает объекты в модели "User_Rate".
    """

    def __init__(self, uow: AbstractUow):
        self.uow = uow

    async def __call__(self, *args, **kwargs):
        pass
