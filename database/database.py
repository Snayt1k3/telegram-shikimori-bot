import pymongo
import os


class DataBase:
    __database = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    __current_db = __database['telegram-shiki-bot']

    @classmethod
    def insert_into_collection(cls, coll: str, data: dict):
        coll = cls.__current_db[coll]
        coll.insert_one(data)

    @classmethod
    def find_one(cls, name: str, value, coll: str) -> dict:
        coll = cls.__current_db[coll]
        return coll.find_one({name: value})

    @classmethod
    def trash_collector(cls, name: str, value: str, coll: str):
        coll = cls.__current_db[coll]
        coll.delete_many({name: value})

    @classmethod
    def update_one(cls, coll, name, value, new_data):
        coll = cls.__current_db[coll]
        coll.update_one({name: value}, {"$set": new_data})

    @classmethod
    def find(cls, coll):
        return cls.__current_db[coll].find()
