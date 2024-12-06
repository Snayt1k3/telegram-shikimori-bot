from shikimori import Shikimori
from src.settings.shiki import shiki_cfg

shiki_client = Shikimori(
    client_secret=shiki_cfg.CLIENT_SECRET,
    user_agent=shiki_cfg.SHIKI_UA,
    client_id=shiki_cfg.CLIENT_ID,
)
