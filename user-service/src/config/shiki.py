from src.config.base import BaseConfig
from pydantic import Field


class ShikimoriConfig(BaseConfig):
    SHIKI_UA: str = Field()
    SHIKI_CLIENT_SECRET: str = Field()
    SHIKI_CLIENT_ID: str = Field()


shiki_cfg = ShikimoriConfig()
