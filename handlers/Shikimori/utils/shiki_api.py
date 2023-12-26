import os

import aiohttp
from aiohttp import ClientSession

from bot import anilibria_client
from database.database import db_repository
from misc.constants import get_headers, SHIKI_URL
from handlers.Shikimori.utils.api_client import BaseApiClient
from database.dto.api_client import Response
from .api_client import ApiClient


class ShikimoriApiClient:
    """
    This class implements requests to shikimori api
    """

    def __init__(self, api_client: BaseApiClient):
        self.client = api_client
        self.url = SHIKI_URL
        self.headers = {"User-Agent": os.getenv("USER_AGENT", None)}

    async def get_anime(self, target_id: str | int) -> Response:
        """
        get info about anime from shikimori by an anime_id
        """
        return await self.client.get(
            f"{self.url}api/animes/{target_id}", headers=self.headers
        )

    async def get_animes_by_status(self, shiki_id: int | str, status: str) -> Response:
        """
        getting a list of animes by status
        :param status: it's name one of lists on shikimori
        :param shiki_id: user id from shikimori
        :return: Response obj
        """

        return await self.client.get(
            f"{self.url}api/v2/user_rates",
            {
                "user_id": shiki_id,
                "target_type": "Anime",
                "status": status,
            },
            self.headers,
        )

    async def get_user_rate(
        self, shiki_id: str | int, target_id: str | int
    ) -> Response:
        """
        :param target_id: id from shikimori
        :param shiki_id: user if from shikimori
        :returns: Response obj
        """

        return await self.client.get(
            f"{self.url}api/v2/user_rates",
            {
                "user_id": shiki_id,
                "target_type": "Anime",
                "target_id": target_id,
            },
            self.headers,
        )

    async def remove_user_rate(
        self, target_id: str | int, shiki_id: str | int
    ) -> Response:
        """
        Delete user rate
        :param target_id: anime id from shikimori
        :param shiki_id: user_id from shikimori
        :returns: Response obj
        """
        anime_rate = await self.get_user_rate(shiki_id, target_id)

        return await self.client.delete(
            f"{self.url}api/v2/user_rates/{anime_rate.text[0]['id']}",
            {"user_rate": {"user_id": id_user, "target_type": "Anime"}},
            {},  # TODO Реализовать Auth
        )

    async def add_anime_rate(
        self, target_id: int | str, shiki_id: int | str, status: str, episodes=0
    ) -> Response:
        """
        create a new anime rate
        :param target_id: id from shikimori
        :param shiki_id: chat_id from tg to find correct user
        :param status: it's name one of lists on shikimori
        :param episodes: number of episodes
        :return: Response obj
        """

        return await self.client.post(
            f"{self.url}api/v2/user_rates",
            {
                "user_rate": {
                    "status": status,
                    "target_id": target_id,
                    "target_type": "Anime",
                    "user_id": shiki_id,
                    "episodes": episodes,
                }
            },
            {},  # TODO Реализовать Auth
        )

    async def update_anime_score(
        self, target_id: int | str, shiki_id: int | str, score
    ) -> Response:
        """
        :param target_id: id from shikimori
        :param shiki_id: user id from shikimori
        :param score: number
        :returns: Response obj
        """
        user_rate = await self.get_user_rate(shiki_id, target_id)
        return await self.client.patch(
            f"{self.url}api/v2/user_rates/{user_rate.text[0]['id']}",
            {
                "user_rate": {
                    "user_id": id_user,
                    "target_type": "Anime",
                    "score": score,
                }
            },
            {},  # TODO Реализовать Auth
        )

    async def update_anime_episodes(
        self, target_id: str | int, shiki_id: str | int, eps=0
    ) -> Response:
        """
        :param target_id: id from shikimori
        :param shiki_id: user id from shikimori
        :param eps: just number episodes, max episodes depends on anime
        """

        user_rate = await self.get_user_rate(shiki_id, target_id)

        return await self.client.patch(
            f"{self.url}api/v2/user_rates/{user_rate.text[0]['id']}",
            {
                "user_rate": {
                    "user_id": shiki_id,
                    "target_type": "Anime",
                    "episodes": eps,
                }
            },
            {},  # TODO Реализовать Auth
        )

    async def search_on_shikimori(self, id_title: int) -> Response:
        """
        make a search by eng title on shikimori from anilibria
        :param id_title: this id from anilibria
        :return: Response obj
        """
        anime_info = await anilibria_client.get_title(id_title)
        return await self.search_by_name(anime_info.names.en)

    async def search_by_name(self, name: str) -> Response:
        """
        Searching on shikimori by name
        :param name: anime title
        :returns: Response obj
        """
        return await self.client.get(
            f"{self.url}api/animes?search={name}&limit=7",
            {},
            self.headers,
        )

    async def get_animes_info(self, target_ids: list) -> Response:
        """
        get info about animes
        :param target_ids: list[target_id from shikimori]
        :return: Response obj
        """
        return await self.client.get(
            f"{self.url}api/animes",
            {"ids": ",".join([str(i) for i in target_ids]), "limit": "50"},
            self.headers,
        )


shiki_api = ShikimoriApiClient(ApiClient())
