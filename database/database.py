import os
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from .schemas.animes import ShikimoriAnime, AnilibriaAnime
from .schemas.user import UserFollows


class DataBase:
    __database = AsyncIOMotorClient(os.environ.get('MONGO_URI'))
    __current_db = __database['telegram-shiki-bot']

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

    @classmethod
    async def get_all_follows(cls) -> List[UserFollows]:
        """
        send all user who subscribe on any anime or exists in collection
        """
        collection = cls.__current_db["user_follows"]
        users = []
        async for user in collection:
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
    async def insert_into_collection(cls, coll: str, data: dict):
        coll = cls.__current_db[coll]
        await coll.insert_one(data)

    @classmethod
    async def find_one(cls, name: str, value, coll: str) -> dict:
        coll = cls.__current_db[coll]
        return coll.find_one({name: value})

    @classmethod
    async def trash_collector(cls, name: str, value: str, coll: str):
        coll = cls.__current_db[coll]
        coll.delete_many({name: value})

    @classmethod
    async def update_one(cls, coll, name, value, new_data):
        coll = cls.__current_db[coll]
        coll.update_one({name: value}, {"$set": new_data})
