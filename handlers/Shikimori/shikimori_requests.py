import os

import aiohttp
from aiohttp import ClientSession

from bot import anilibria_client
from database.database import DataBase
from misc.constants import get_headers, SHIKI_URL


class ShikimoriRequests:
    """
    This class implements logic on request to shikimori website
    """

    SHIKI = SHIKI_URL
    SESSION = ClientSession(headers={"User-Agent": os.getenv("USER_AGENT", None)})

    @classmethod
    async def GetAnimeInfo(cls, target_id) -> dict:
        """
        get info user_rate by target id
        :param target_id: id from shikimori
        :return dict
        """
        async with cls.SESSION.get(f"{cls.SHIKI}api/animes/{target_id}") as response:
            if response.status == 200:
                return await response.json()
            return {}

    @classmethod
    async def GetAnimesByStatusId(cls, chat_id, status) -> list[dict]:
        """
        getting a list of animes by status and user_id(chat_id)
        :param status: it's name one of lists on shikimori
        :param chat_id: chat_id from tg to find correct user
        :return list
        """
        id_user = await cls.GetShikiId(chat_id)
        async with cls.SESSION.get(
            f"{cls.SHIKI}"
            f"api/v2/user_rates?user_id={id_user}&"
            f"target_type=Anime&status={status}"
        ) as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def GetAnimeInfoRate(cls, chat_id, target_id) -> list[dict]:
        """
        :param target_id: id from shikimori
        :param chat_id: chat_id from tg to find correct user
        :return list with one dict
        """
        id_user = await cls.GetShikiId(chat_id)
        async with cls.SESSION.get(
            f"{cls.SHIKI}api/v2/user_rates?user_id={id_user}&"
            f"target_type=Anime&target_id={target_id}"
        ) as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def DeleteAnimeProfile(cls, target_id, chat_id) -> int:
        """
        Delete user rate
        :param target_id: id from shikimori
        :param chat_id: chat_id from tg to find correct user
        :return HTTP status code
        """
        id_user = await cls.GetShikiId(chat_id)
        anime_id = await cls.GetAnimeInfoRate(chat_id, target_id)

        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.delete(
                f"{cls.SHIKI}api/v2/user_rates/{anime_id[0]['id']}",
                json={"user_rate": {"user_id": id_user, "target_type": "Anime"}},
            ) as response:
                return response.status

    @classmethod
    async def AddAnimeRate(cls, target_id, chat_id, status, episodes=0) -> int:
        """
        create a new anime rate
        :param target_id: id from shikimori
        :param chat_id: chat_id from tg to find correct user
        :param status: it's name one of lists on shikimori
        :param episodes: just number episodes, max episodes depends on anime
        :return: HTTP status code
        """
        id_user = await cls.GetShikiId(chat_id)
        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.post(
                f"{cls.SHIKI}api/v2/user_rates",
                json={
                    "user_rate": {
                        "status": status,
                        "target_id": target_id,
                        "target_type": "Anime",
                        "user_id": id_user,
                        "episodes": episodes,
                    }
                },
            ) as response:
                return response.status

    @classmethod
    async def UpdateAnimeScore(cls, target_id, chat_id, score=0) -> dict:
        """
        :param target_id: id from shikimori
        :param chat_id: chat_id from tg to find correct user
        :param score: just number, max - 10
        """
        id_user = await cls.GetShikiId(chat_id)
        info_target = await cls.GetAnimeInfoRate(chat_id, target_id)

        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.patch(
                cls.SHIKI + f"api/v2/user_rates/{info_target[0]['id']}",
                json={
                    "user_rate": {
                        "user_id": id_user,
                        "target_type": "Anime",
                        "score": score,
                    }
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}

    @classmethod
    async def UpdateAnimeEps(cls, target_id, chat_id, eps=0):
        """
        :param target_id: id from shikimori
        :param chat_id: chat_id from tg to find correct user
        :param eps: just number episodes, max episodes depends on anime
        """

        id_user = await cls.GetShikiId(chat_id)
        info_target = await cls.GetAnimeInfoRate(chat_id, target_id)

        async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
            async with session.patch(
                cls.SHIKI + f"api/v2/user_rates/{info_target[0]['id']}",
                json={
                    "user_rate": {
                        "user_id": id_user,
                        "target_type": "Anime",
                        "episodes": eps,
                    }
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}

    @classmethod
    async def SearchShikimori(cls, id_title) -> list[dict]:
        """
        make a search by eng title on shikimori from anilibria
        :param id_title: this id from anilibria.tv not from shikimori
        :return: list of animes which founds
        """
        anime_info = await anilibria_client.get_title(id_title)

        async with cls.SESSION.get(
            cls.SHIKI + f"api/animes?search=" f"{anime_info.names.en}&limit=7"
        ) as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def SearchShikimoriTitle(cls, title) -> list[dict]:
        """
        Searching on shikimori by title name
        :param title: anime title
        :return : list with anime which found
        """
        async with cls.SESSION.get(
            cls.SHIKI + f"api/animes?search=" f"{title}&limit=7"
        ) as response:
            if response.status == 200:
                return await response.json()
            return []

    @classmethod
    async def GetShikiId(cls, chat_id) -> str:
        """
        get shiki id from db
        :param chat_id: chat_id from telegram
        :return :str
        """
        try:
            res = await DataBase.find_one("chat_id", chat_id, "users_id")
            return res.get("shikimori_id")
        except Exception:
            return ""

    @classmethod
    async def GetAnimesInfo(cls, target_ids: list) -> list[dict]:
        """
        get info about animes
        :param target_ids: list[target_id from shikimori]
        :return: list with dicts
        """
        if target_ids:
            async with cls.SESSION.get(
                f"{cls.SHIKI}api/animes?ids={','.join([str(i) for i in target_ids])}&limit=8"
            ) as response:
                return await response.json()
        else:
            return []
