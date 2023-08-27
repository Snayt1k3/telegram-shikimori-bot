import os
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from .schemas.animes import ShikimoriAnime, AnilibriaAnime
from .schemas.user import UserFollows


class DataBase:
    __database = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
    _current_db = __database["telegram-shiki-bot"]

    @classmethod
    async def insert_into_collection(cls, coll: str, data: dict):
        coll = cls._current_db[coll]
        await coll.insert_one(data)

    @classmethod
    async def find(cls, coll: str):
        coll = cls._current_db[coll]
        return coll.find()

    @classmethod
    async def find_one(cls, name: str, value, coll: str) -> dict:
        coll = cls._current_db[coll]
        obj = await coll.find_one({name: value})
        return obj

    @classmethod
    async def trash_collector(cls, name: str, value, coll: str):
        coll = cls._current_db[coll]
        await coll.delete_many({name: value})

    @classmethod
    async def update_one(cls, coll, name, value, new_data):
        coll = cls._current_db[coll]
        await coll.update_one({name: value}, {"$set": new_data})
