import pymongo
import os


class DataBase:
    __database = pymongo.MongoClient(os.environ.get('MONGO_URI'))
    __current_db = __database['telegram-shiki-bot']

    def insert_into_collection(self, coll: str, data: dict):
        coll = self.__current_db[coll]
        coll.insert_one(data)

    def find_one(self, name: str, value, coll:str) -> dict:
        coll = self.__current_db[coll]
        return coll.find_one({name: value})

    def trash_collector(self, name: str, value: str, coll: str):
        coll = self.__current_db[coll]
        coll.delete_many({name: value})

    def update_one(self, coll, name, value, new_data):
        coll = self.__current_db[coll]
        coll.update_one({name: value}, {"$set": new_data})

    def find(self, coll):
        return self.__current_db[coll].find()