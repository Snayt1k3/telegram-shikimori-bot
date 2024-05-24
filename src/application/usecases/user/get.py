from src.application.interfaces.usecases.base import UseCase


class GetAllUserRatesUseCase(UseCase):
    """
    getting a current user rates from profile
    """

    def __call__(self, obj: "DTO"):  # TODO добавить DTO
        pass


class GetCredentialsUseCase(UseCase):
    """
    getting a credentials for shikimori oauth
    """

    def __call__(self, obj: "DTO"):  # TODO добавить DTO
        pass


