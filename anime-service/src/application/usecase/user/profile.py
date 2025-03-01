from shikimori import Shikimori

from src.application.dto.user import UserProfileDTO
from src.application.interfaces import AbstractUow
from src.application.interfaces.usecase import UseCase


class UserProfile(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, user_id: int) -> UserProfileDTO:
        return UserProfileDTO()
