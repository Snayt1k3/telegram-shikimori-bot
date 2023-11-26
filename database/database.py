import logging
import os
from typing import List
from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection as Collection

from .schemas.animes import ShikimoriAnime, AnilibriaAnime
from .schemas.user import UserFollows


class BaseRepository(ABC):
    @abstractmethod
    async def create_one(self, collection: str, data: dict):
        """
        create one record in db

        :param collection: name of collection
        :param data: new record
        """
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, collection: str, filter: dict, new_data: dict):
        """
        update one record by filter

        :param collection: Name of collection
        :param filter: query
        :param new_data: new record
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, collection: str, filter: dict):
        """
        delete one record by filter

        :param collection: Name of collection
        :param filter: query
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, collection: str, filter: dict):
        """
        delete records by filter

        :param collection: Name of collection
        :param filter: query
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, collection: str, filter: dict):
        """
        get record from collection by filter

        :param collection: Name of collection
        :param filter: query
        """
        raise NotImplementedError


class MongoRepository(BaseRepository):
    def __init__(self):
        self._database = AsyncIOMotorClient(os.environ.get("MONGO_URI_DEV"))
        self._current_db = self._database["telegram-shiki-bot"]

    async def create_one(self, collection: str, data: dict):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.insert_one(data)
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")

    async def update_one(self, collection: str, filter: dict, new_data: dict):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.update_one(filter=filter, update={"$set": new_data})
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")

    async def get_one(self, collection: str, filter: dict):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.find_one(filter=filter)
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")

    async def delete_many(self, collection: str, filter: dict):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.delete_many(filter=filter)
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")

    async def delete_one(self, collection: str, filter: dict):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.delete_one(filter=filter)
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")

    async def find(self, collection):
        try:
            collection: Collection = self._current_db[collection]
            obj = await collection.find()
            return obj
        except Exception as e:
            logging.error(f"Error occurred in repository - {e}")


db_repository = MongoRepository()
