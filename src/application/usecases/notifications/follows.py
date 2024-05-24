from src.application.interfaces.usecases.base import UseCase


class AddFollowUseCase(UseCase):
    """
    add follow on anime(anilibria)
    """

    def __call__(self, obj: "UpdateDTO"):  # TODO добавить DTO и таблицу
        pass


class DeleteFollowUseCase(UseCase):
    """
    deleting follow on anime for user
    """

    def __call__(self, obj: "UserRateUpdateDTO"):  # TODO добавить DTO и таблицу
        pass

class GetAllFollowsUseCase(UseCase):
    """
    get all follows
    """

    def __call__(self, id: int):  # TODO добавить DTO и таблицу
        pass


