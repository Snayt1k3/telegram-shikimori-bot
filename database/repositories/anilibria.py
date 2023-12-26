import logging
from typing import List

import orjson
from anilibria import Title

from bot import anilibria_client
from database.database import MongoRepository
from database.dto.animes import AnilibriaAnime, ShikimoriAnime
from database.dto.user import UserFollows


class AnilibriaRepository(MongoRepository):
    """
    logic with anime Anilibria
    """

    async def subscribe_notifications(
        self, title_id: int, chat_id: int
    ) -> AnilibriaAnime | None | str:
        """
        add title_id in user follows
        :param title_id: Anilibria id
        :param chat_id: Telegram chat_id
        :return: if OK return AnilibriaAnime else None if error and str if user already followed
        """
        try:
            anime = await anilibria_client.get_title(title_id)
            anime_obj = AnilibriaAnime(
                id=anime.id, title_en=anime.names.en, title_ru=anime.names.ru
            )
            user = await super().get_one("user_follows", {"chat_id": chat_id})

            if not user or not user["animes"]:
                await super().create_one(
                    "user_follows",
                    {
                        "chat_id": chat_id,
                        "animes": [orjson.loads(anime_obj.model_dump_json())],
                    },
                )

            else:
                animes = user["animes"]
                for anime in animes:
                    if title_id == anime["id"]:
                        return f"Вы уже подписаны на аниме - {anime['title_ru']}"
                animes.append(orjson.loads(anime_obj.model_dump_json()))
                await super().update_one(
                    "user_follows",
                    {
                        "chat_id": chat_id,
                    },
                    {"animes": animes},
                )

            return anime_obj
        except Exception as e:
            logging.error(
                f"Error occurred when user trying to subscribe notifications - {e}"
            )

    async def unsubscribe_notifications(
        self, title_id: int, chat_id: int
    ) -> AnilibriaAnime | None:
        """
        remove title_id from user follows
        :param title_id: Anilibria title id
        :param chat_id: Telegram chat_id
        """
        try:
            user = await super().get_one(
                filter={"chat_id": chat_id}, collection="user_follows"
            )

            if not user:
                return None
            animes = user["animes"]
            for i, title in enumerate(animes):
                if title["id"] == title_id:
                    del animes[i]

                    anime = AnilibriaAnime(**title)

                    await super().update_one(
                        "user_follows", {"chat_id": chat_id}, {"animes": animes}
                    )

                    return anime
            return None

        except Exception as e:
            logging.error(
                f"Error occurred when user trying unsubscribe notifications - {e}"
            )

    async def get_all_follows(self) -> list[UserFollows]:
        """
        send all user who subscribe on any anime or exists in collection
        """
        collection = await super().find("user_follows")
        users = []
        async for user in collection:
            users.append(
                UserFollows(
                    chat_id=user.get("chat_id"),
                    follows=[AnilibriaAnime(**anime) for anime in user["animes"]],
                )
            )
        return users

    async def get_all_follows_by_user(self, chat_id: int) -> UserFollows | None:
        """
        get one user follows
        :param chat_id: Telegram chat_id
        :return: one obj of user_follows or none if not exists
        """
        try:
            follows = await super().get_one("user_follows", {"chat_id": chat_id})

            if not follows:
                return

            obj = UserFollows(
                chat_id=follows.get("chat_id"),
                follows=follows.get("animes"),
            )
            return obj
        except Exception as e:
            logging.error(
                f"Error occurred when trying to get user_follows from db - {e}"
            )

    async def insert_anilibria_list(
        self, chat_id: int, collection: str, animes: list[Title]
    ) -> list[dict]:
        """
        insert anilibria objects, but before deleted previous objects
        :param chat_id: Telegram chat_id
        :param collection: Name of mongo collection
        :param animes: List of obj Title from anilibria
        """

        try:
            await super().delete_many(collection, {"chat_id": chat_id})

            anime_list = [
                {
                    "id": anime.id,
                    "title_ru": anime.names.ru,
                    "title_en": anime.names.en,
                }
                for anime in animes
            ]

            await super().create_one(
                collection, {"chat_id": chat_id, "animes": anime_list}
            )

            return animes

        except Exception as e:
            logging.error(
                f"Error occurred when trying to insert anilibria_list into db - {e}"
            )

    async def get_anilibria_list(
        self, chat_id: int, collection: str
    ) -> list[AnilibriaAnime]:
        """
        :param chat_id: Telegram chat id
        :param collection: name of Mongo collections
        """
        try:
            obj = await super().get_one(collection, {"chat_id": chat_id})
            animes = [AnilibriaAnime(**anime) for anime in obj["animes"]]
            return animes
        except Exception as e:
            logging.error(
                f"Error occurred when trying to get anilibria_list from db - {e}"
            )


anilibria_repository = AnilibriaRepository()
