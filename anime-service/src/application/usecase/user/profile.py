from shikimori import Shikimori
from shikimori.exceptions import RequestError

from src.application.dto import UserProfileDTO
from src.application.interfaces import AbstractUow, UseCase


class UserProfile(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self._uow = uow
        self._shiki = shiki

    async def __call__(self, user_id: int) -> UserProfileDTO:
        response = await self._shiki.user.ById(user_id)

        if isinstance(response, RequestError):
            raise response

        anime_stats = {}
        manga_stats = {}

        for entry in response.stats.statuses.animes:
            anime_stats[entry.name] = entry.size

        for entry in response.stats.statuses.manga:
            manga_stats[entry.name] = entry.size

        return UserProfileDTO(
            mangas=manga_stats,
            animes=anime_stats,
            username=response.nickname,
            avatar=response.image.x160
        )

