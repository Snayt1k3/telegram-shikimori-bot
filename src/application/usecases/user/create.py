
from src.application.interfaces.usecases.base import UseCase


class AddUserUseCase(UseCase):
    """
    adding new user to db with his user rates from shikimori
    """
    def __call__(self, code: str, id_telegram: int):
        pass

class AddUserRateUseCase(UseCase):
    def __call__(self, obj: "UserRateDTOCreate"):  # todo добавить create dto
        pass
