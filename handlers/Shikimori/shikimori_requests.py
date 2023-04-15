import os

import aiohttp
from aiohttp import ClientSession

from handlers.Anilibria.helpful_functions import get_anime_info_from_al
from misc.constants import get_headers, shiki_url


class ShikimoriRequests:
    SHIKI = shiki_url
    SESSION = ClientSession(headers={'User-Agent': os.getenv(USER_AGENT, None)})

    @classmethod
    async def get_info_anime_from_shiki(cls, target_id) -> dict:
        async with cls.SESSION as session:
            async with session.get(f"{cls.SHIKI}api/animes/{target_id}") as response:
                if response.status == 200:
                    return await response.json()
                return {}

    @classmethod
    async def get_animes_by_status_and_id(cls, chat_id: int, status: str) -> list[dict]:
        """
        getting a list of animes by status and user_id(chat_id)
        """
        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)
        async with cls.SESSION as session:
            async with session.get(f"{cls.SHIKI}"
                                   f"api/v2/user_rates?user_id={id_user}&"
                                   f"target_type=Anime&status={status}") as response:
                if response.status == 200:
                    return await response.json()
                return []

    @classmethod
    async def get_anime_info_user_rate(cls, chat_id: int, target_id) -> list[dict]:
        """
        this method make a get request
        :return list with one dict
        """

        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)

        # make a request
        async with cls.SESSION as session:
            async with session.get(
                    f"{cls.SHIKI}api/v2/user_rates?user_id={id_user}&"
                    f"target_type=Anime&target_id={target_id}") as response:
                if response.status == 200:
                    return await response.json()
                return []

    @classmethod
    async def delete_anime_from_user_profile(cls, target_id, chat_id: int) -> int:
        """
        This function delete an anime from user profile on shikimori
        :return response.status_code
        """

        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)
        anime_id = await get_anime_info_user_rate(chat_id, target_id)

        # make request
        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.delete(f"{cls.SHIKI}api/v2/user_rates/{anime_id[0]['id']}",
                                      json={
                                          "user_rate": {
                                              "user_id": id_user,
                                              "target_type": "Anime"
                                          }
                                      }) as response:
                return response.status

    @classmethod
    async def add_anime_rate(cls, target_id, chat_id, status, episodes=0) -> int:
        """
        This function add an anime into profile user on shikimori
        :return response.status_code
        """
        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)

        # make a request
        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.post(
                    f"{cls.SHIKI}api/v2/user_rates", json={
                        "user_rate": {
                            "status": status,
                            "target_id": target_id,
                            "target_type": "Anime",
                            "user_id": id_user,
                            "episodes": episodes
                        }
                    }) as response:
                return response.status

    @classmethod
    async def update_anime_score(cls, target_id, chat_id, score: int = 0) -> dict:
        """This function make a patch request, if we have score, score can be updated"""

        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)
        info_target = await get_anime_info_user_rate(chat_id, target_id)

        # make a request
        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.patch(
                    cls.SHIKI + f"api/v2/user_rates/{info_target[0]['id']}",
                    json={"user_rate": {
                        "user_id": id_user,
                        "target_type": "Anime",
                        "score": score
                    }}) as response:

                if response.status == 200:
                    return await response.json()
                return {}

    @classmethod
    async def update_anime_eps(cls, target_id, chat_id, eps=0):
        """This function make a patch request, if we have eps, eps can be updated"""

        # get require data
        id_user = await get_shiki_id_by_chat_id(chat_id)
        info_target = await get_anime_info_user_rate(chat_id, target_id)

        # make a request
        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.patch(
                    cls.SHIKI + f"api/v2/user_rates/{info_target[0]['id']}",
                    json={"user_rate": {
                        "user_id": id_user,
                        "target_type": "Anime",
                        "episodes": eps
                    }}) as response:

                if response.status == 200:
                    return await response.json()
                return {}

    @classmethod
    async def search_on_shikimori(cls, id_title) -> list[dict]:
        """
        :param id_title: this id from anilibria.tv not from shikimori
        :return: list of animes which founds
        """
        # get require data
        anime_info = await get_anime_info_from_al(id_title)

        # make a request
        async with cls.SESSION as session:
            async with session.get(cls.SHIKI + f"api/animes?search="
                                               f"{anime_info['names']['en']}&limit=7") as response:

                if response.status == 200:
                    return await response.json()
                return []
