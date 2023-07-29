import json
import logging
from typing import List

from bot import anilibria_client
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
        :return: if OK return AnilibriaAnime else None if error
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
                    {"chat_id": chat_id, "animes": [json.loads(anime_obj.model_dump_json())]}
                )

            else:
                animes = user['animes']
                for anime in animes:
                    if title_id == anime['id']:
                        return f"Вы уже подписаны на аниме - <i>{anime['title_ru']}</i>"
                animes.append(json.loads(anime_obj.model_dump_json()))
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
    async def insert_anime_list(
            cls,
            collection: str,
            animes: List[ShikimoriAnime] | List[AnilibriaAnime]
    ) -> None:
        """
        :param collection: Mongo collection
        :param animes: objs anime list
        """
        try:
            collection = cls.__current_db[collection]
            await collection.insert_one(
                {
                    'chat_id': animes.chat_id,
                    'animes': animes
                }
            )
        except Exception:
            pass
