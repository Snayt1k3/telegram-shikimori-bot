from shikimori.client import Shikimori

from src.application.dto.user.auth import ShikiCredsCreateDTO
from src.application.interfaces.database.uow.base import AbstractUnitOfWork
from src.application.interfaces.usecases.base import UseCase


class NewCredentialsUseCase(UseCase):
    """
    getting credentials from db, if creds is expired, they will update
    """

    def __init__(self, shiki: Shikimori, uow: AbstractUnitOfWork):
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, id_telegram: int) -> ShikiCredsCreateDTO:
        pass
