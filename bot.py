import logging
import os
import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
API_TOKEN = os.environ.get("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure DB
db_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
