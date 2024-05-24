from src.application.interfaces.usecases.base import UseCase


class GetTorrentUseCase(UseCase):
    """
    get a torrent url from anilibria
    """

    def __call__(self, obj: "UpdateDTO"):  # TODO добавить DTO
        pass


