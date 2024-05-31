import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv

load_dotenv("./misc/.env")

API_TOKEN = os.environ.get("TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",  # msg form
    handlers=[logging.StreamHandler(), logging.FileHandler("bot.log")],  # console
)

# Initialize bot, dispatcher and other
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
    