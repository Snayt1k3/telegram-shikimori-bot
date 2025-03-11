from src.config.base import BaseConfig
from pydantic import Field


class ShikimoriSettings(BaseConfig):
    SHIKI_UA: str = Field(
        description="Shikimori user agent represents access to shikimori api",
    )
    SHIKI_CLIENT_SECRET: str = Field()
    SHIKI_CLIENT_ID: str = Field()


shiki_cfg = ShikimoriSettings()
