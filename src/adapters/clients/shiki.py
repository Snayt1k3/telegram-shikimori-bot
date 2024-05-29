from shikimori.client import Shikimori
from src.adapters.common.config import ShikimoriCfg

shiki_client = Shikimori(
    user_agent=ShikimoriCfg.SHIKI_UA,
    client_id=ShikimoriCfg.CLIENT_ID,
    client_secret=ShikimoriCfg.CLIENT_SECRET,
)
