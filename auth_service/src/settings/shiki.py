from src.settings.base import Settings
from pydantic import Field


class ShikimoriSettings(Settings):
    SHIKI_UA: str = Field(
        description="Shikimori user agent represents access to shikimori api",
    )
    SHIKI_CLIENT_SECRET: str = Field()
    SHIKI_CLIENT_ID: str = Field()


shiki_cfg = ShikimoriSettings()
