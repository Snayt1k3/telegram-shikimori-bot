from src.application.interfaces.usecases.base import UseCase


class GetUserListUseCase(UseCase):
    """
    getting user list from shikimori and inserting hin into redis
    """

    def __call__(self, obj: "UpdateDTO"):  # TODO добавить DTO
        pass


class PaginationUseCase(UseCase):
    """
    getting list from redis, if data is expired, request to a new data
    """

    def __call__(self, obj: "PaginationDTO"):  # TODO добавить DTO
        pass



