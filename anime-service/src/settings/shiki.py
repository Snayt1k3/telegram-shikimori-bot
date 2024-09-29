from src.settings.base import Settings
from pydantic import Field


class ShikimoriSettings(Settings):
    SHIKI_UA: str = Field(
        description="Shikimori user agent represents access to shikimori api",
        alias="USER_AGENT",
    )
    SHIKI_CLIENT_SECRET: str = Field(alias="CLIENT_SECRET")
    SHIKI_CLIENT_ID: str = Field(alias="CLIENT_ID")
