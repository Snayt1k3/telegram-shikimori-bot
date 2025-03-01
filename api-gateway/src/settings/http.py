from pydantic import Field

from src.config.base import BaseConfig


class HttpSettings(BaseConfig):
    AUTH_URL: str = Field()


http_settings = HttpSettings()
