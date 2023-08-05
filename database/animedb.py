import logging
from typing import List

import orjson
from anilibria import Title

from bot import anilibria_client
from handlers.Shikimori.shikimori_requests import ShikimoriRequests
from .database import DataBase
from .schemas.animes import AnilibriaAnime, ShikimoriAnime
from .schemas.user import UserFollows


class AnimeDB(DataBase):
    """
    logic with anime titles
    """

    @classmethod
    async def subscribe_notifications(cls, title_id: int, chat_id: int) -> AnilibriaAnime | None | str:
        """
        add title_id in user follows
        :param title_id: Anilibria id
        :param chat_id: Telegram chat_id
        :return: if OK return AnilibriaAnime else None if error and str if user already followed
        """
        try:
            # create insert obj
            anime = await anilibria_client.get_title(title_id)
            anime_obj = AnilibriaAnime(
                id=anime.id,
                title_en=anime.names.en,
                title_ru=anime.names.ru
            )

            # searching user
            user = await super().find_one("chat_id", chat_id, "user_follows")

            # check user exists and animes is not None
            if not user or not user['animes']:
                await super().insert_into_collection(
                    "user_follows",
                    {"chat_id": chat_id, "animes": [orjson.loads(anime_obj.model_dump_json())]}
                )

            else:
                animes = user['animes']
                for anime in animes:
                    if title_id == anime['id']:
                        return f"Вы уже подписаны на аниме - <i>{anime['title_ru']}</i>"
                animes.append(orjson.loads(anime_obj.model_dump_json()))
                await super().update_one(
                    "user_follows",
                    "chat_id",
                    chat_id,
                    {"animes": animes},
                )

            return anime_obj
        except Exception as e:
            logging.error(f"Error occurred when user trying to subscribe notifications - {e}")
            return None

    @classmethod
    async def unsubscribe_notifications(cls, title_id: int, chat_id: int) -> AnilibriaAnime | None:
        """
        remove title_id from user follows
        :param title_id: Anilibria title id
        :param chat_id: Telegram chat_id
        """
        try:
            user = await super().find_one("chat_id", chat_id, "user_follows")

            if not user:
                return None
            animes = user['animes']
            for i, title in enumerate(animes):
                if title['id'] == title_id:
                    # remove anime
                    del animes[i]

                    # get object for return
                    anime = AnilibriaAnime(**title)

                    # db updates
                    await super().update_one(
                        'user_follows',
                        "chat_id",
                        chat_id,
                        {"animes": animes})

                    return anime
            return None

        except Exception as e:
            logging.error(f"Error occurred when user trying unsubscribe notifications - {e}")
            return None

    @classmethod
    async def get_all_follows(cls) -> List[UserFollows]:
        """
        send all user who subscribe on any anime or exists in collection
        """
        collection = await super().find("user_follows")
        users = []
        for user in collection:
            users.append(
                UserFollows(
                    chat_id=user.get('chat_id'),
                    follows=[AnilibriaAnime(
                        title_ru=anime.get('title_ru'),
                        title_en=anime.get('title_en'),
                        id=anime.get('id')
                    )
                        for anime in user['animes']]
                )
            )
        return users

    @classmethod
    async def get_all_follows_by_user(cls, chat_id: int) -> UserFollows | None:
        """
        get one user follows
        :param chat_id: Telegram chat_id
        :return: one obj of user_follows or none if not exists
        """
        try:
            follows = await super().find_one("chat_id", chat_id, 'user_follows')

            if not follows:
                return None

            obj = UserFollows(
                chat_id=follows.get("chat_id"),
                follows=follows.get('animes'),
            )
            return obj
        except Exception as e:
            logging.error(f"Error occurred when trying to get user_follows from db - {e}")
            return None

    @classmethod
    async def insert_shiki_list(cls, chat_id: int, collection: str, anime_ids: List[int]) -> List[ShikimoriAnime]:
        """
        insert shiki ids in db, but before deleted previous objs
        :param chat_id: telegram chat_id
        :param collection: Mongo Collection
        :param anime_ids: List of anime shiki responses
        """
        try:
            animes_info = await ShikimoriRequests.GetAnimesInfo(anime_ids[:8])
            animes = []
            for anime in animes_info:
                animes.append(ShikimoriAnime(
                    title_ru=anime['russian'],
                    title_en=anime['name'],
                    id=anime['id'],
                ))

            await super().trash_collector("chat_id", chat_id, collection)
            await super().insert_into_collection(
                collection,
                {
                    "chat_id": chat_id,
                    "animes": anime_ids
                }
            )
            return animes
        except Exception as e:
            logging.error(f"Error occurred when trying to insert shikilist into db - {e}")

    @classmethod
    async def get_shiki_list(cls, chat_id: int, collection: str, page: int) -> List[ShikimoriAnime]:
        """
        :param chat_id: Telegram chat id
        :param collection: name of Mongo collection
        :param page: page
        """
        try:
            page = int(page)
            obj = await super().find_one("chat_id", chat_id, collection)

            animes = await ShikimoriRequests.GetAnimesInfo(obj['animes'][page:page + 8])
            shiki_animes = []

            for anime in animes:
                shiki_animes.append(ShikimoriAnime(
                    title_ru=anime['russian'],
                    title_en=anime['name'],
                    id=anime['id'],
                ))

            return shiki_animes

        except Exception as e:
            logging.error(f"Error occurred when trying to get info about anime form shiki - {e}")

    @classmethod
    async def insert_anilibria_list(cls, chat_id: int, collection: str, animes: List[Title]) -> List[Title]:
        """
        insert anilibria objects, but before deleted previous objects
        :param chat_id: Telegram chat_id
        :param collection: Name of mongo collection
        :param animes: List of obj Title from anilibria
        """

        try:
            # delete previous objs
            await super().trash_collector("chat_id", chat_id, collection)

            # getting data
            anime_list = []

            for anime in animes:
                anime_list.append(
                    {
                        "id": anime.id,
                        "title_ru": anime.names.ru,
                        "title_en": anime.names.en,
                    }
                )

            # inserting
            await super().insert_into_collection(collection, {
                "chat_id": chat_id,
                "animes": anime_list
            })

            return animes

        except Exception as e:
            logging.error(f"Error occurred when trying to insert anilibria_list into db - {e}")

    @classmethod
    async def get_anilibria_list(cls, chat_id: int, collection: str) -> List[AnilibriaAnime]:
        """
        :param chat_id: Telegram chat id
        :param collection: name of Mongo collections
        """
        try:
            obj = await super().find_one("chat_id", chat_id, collection)
            animes = []

            for anime in obj['animes']:
                animes.append(AnilibriaAnime(
                    title_en=anime['title_en'],
                    title_ru=anime['title_ru'],
                    id=anime['id'],
                ))

            return animes
        except Exception as e:
            logging.error(f"Error occurred when trying to get anilibria_list from db - {e}")
