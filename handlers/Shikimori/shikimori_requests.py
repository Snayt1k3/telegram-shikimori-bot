import asyncio
import os

import aiohttp
from aiohttp import ClientSession
from database.database import DataBase
from handlers.Anilibria.helpful_functions import get_anime_info_from_al
from misc.constants import get_headers, SHIKI_URL


class ShikimoriRequests:
    SHIKI = SHIKI_URL
    SESSION = ClientSession(headers={'User-Agent': os.getenv('USER_AGENT', None)})
    SEMAPHORE = asyncio.Semaphore(5)

    @classmethod
    async def GetAnimeInfo(cls, target_id) -> dict:
        async with cls.SESSION.get(f"{cls.SHIKI}api/animes/{target_id}") as response:
            if response.status == 200:
                return await response.json()
            return {}

    @classmethod
    async def GetAnimesByStatusId(cls, chat_id, status) -> list[dict]:
        """
        getting a list of animes by status and user_id(chat_id)
        """
        # get require data
        id_user = await cls.GetShikiId(chat_id)
        async with cls.SESSION.get(f"{cls.SHIKI}"
                                   f"api/v2/user_rates?user_id={id_user}&"
                                   f"target_type=Anime&status={status}") as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def GetAnimeInfoRate(cls, chat_id, target_id) -> list[dict]:
        """
        this method make a get request
        :return list with one dict
        """
        id_user = await cls.GetShikiId(chat_id)
        async with cls.SESSION.get(
                f"{cls.SHIKI}api/v2/user_rates?user_id={id_user}&"
                f"target_type=Anime&target_id={target_id}") as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def DeleteAnimeProfile(cls, target_id, chat_id) -> int:
        """
        This function delete an anime from user profile on shikimori
        :return response.status_code
        """
        id_user = await cls.GetShikiId(chat_id)
        anime_id = await cls.GetAnimeInfoRate(chat_id, target_id)

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
    async def AddAnimeRate(cls, target_id, chat_id, status, episodes=0) -> int:
        """
        This function add an anime into profile user on shikimori`
        """
        id_user = await cls.GetShikiId(chat_id)
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
    async def UpdateAnimeScore(cls, target_id, chat_id, score=0) -> dict:
        """This function make a patch request, if we have score, score can be updated"""
        id_user = await cls.GetShikiId(chat_id)
        info_target = await cls.GetAnimeInfoRate(chat_id, target_id)

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
    async def UpdateAnimeEps(cls, target_id, chat_id, eps=0):
        """This function make a patch request, if we have eps, eps can be updated"""

        id_user = await cls.GetShikiId(chat_id)
        info_target = await cls.GetAnimeInfoRate(chat_id, target_id)

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
    async def SearchShikimori(cls, id_title) -> list[dict]:
        """
        :param id_title: this id from anilibria.tv not from shikimori
        :return: list of animes which founds
        """
        anime_info = await get_anime_info_from_al(id_title)

        async with cls.SESSION.get(cls.SHIKI + f"api/animes?search="
                                               f"{anime_info['names']['en']}&limit=7") as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def SearchShikimoriTitle(cls, title) -> list[dict]:
        """Searching on shikimori by title name"""
        async with cls.SESSION.get(cls.SHIKI + f"api/animes?search="
                                               f"{title}&limit=7") as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def GetShikiId(cls, chat_id):
        try:
            return DataBase.find_one('chat_id', chat_id, 'users_id')['shikimori_id']
        except TypeError:
            return ''

    @classmethod
    async def GetAnimeSemaphore(cls, target_id):
        await cls.SEMAPHORE.acquire()
        await asyncio.sleep(1)
        async with cls.SESSION.get(f"{cls.SHIKI}api/animes/{target_id}") as response:
            cls.SEMAPHORE.release()
            return await response.json(content_type=None)
