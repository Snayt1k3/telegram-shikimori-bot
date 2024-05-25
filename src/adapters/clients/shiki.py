from shikimori.client import Shikimori
from src.adapters.common.config import Config

shiki_client = Shikimori(
    user_agent=Config.SHIKI_UA,
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
)
