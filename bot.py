import logging
import os
import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# for dev
from dotenv import load_dotenv
load_dotenv('./misc/.env')
API_TOKEN = os.environ.get("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
