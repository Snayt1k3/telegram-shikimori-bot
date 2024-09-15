from shikimori import Shikimori
from src.config import Config

shiki_client = Shikimori(
    client_secret=Config.CLIENT_SECRET,
    user_agent=Config.SHIKI_UA,
    client_id=Config.CLIENT_ID,
)
