import logging
import os
import pymongo
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from anilibria import AniLibriaClient

load_dotenv('./misc/.env')

API_TOKEN = os.environ.get("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',  # msg form
                    handlers=[
                        logging.StreamHandler()  # console
                    ])

# Initialize bot, dispatcher and other
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=storage)
anilibria_client = AniLibriaClient()
