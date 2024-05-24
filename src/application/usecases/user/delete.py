from src.application.interfaces.usecases.base import UseCase


class DeleteUserUseCase(UseCase):
    """
    delete user from db
    """

    def __call__(self, id: int):
        pass


class DeleteUserRateUseCase(UseCase):
    """
    delete user_rate from db and shikimori
    """

    def __call__(self, id: int):
        pass
