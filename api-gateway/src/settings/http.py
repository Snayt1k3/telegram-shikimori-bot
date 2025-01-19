from pydantic import Field

from src.settings.base import Settings


class HttpSettings(Settings):
    AUTH_URL: str = Field()


http_settings = HttpSettings()
