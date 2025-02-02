from pydantic import Field
from src.config.base import Settings


class HttpSettings(Settings):
    AUTH_URL: str = Field()


http_settings = HttpSettings()
