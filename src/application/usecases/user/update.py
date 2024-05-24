from src.application.interfaces.usecases.base import UseCase


class UpdateUserUseCase(UseCase):
    """
    update user in db
    """

    def __call__(self, obj: "DTO"):  # TODO добавить DTO
        pass


class UpdateUserRateUseCase(UseCase):
    """
    update user_rate in db and shikimori
    """

    def __call__(self, obj: "DTO"):  # TODO добавить DTO
        pass


