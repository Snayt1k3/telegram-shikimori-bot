from pydantic import Field

from src.config.base import BaseConfig


class BotSettings(BaseConfig):
    API_TOKEN: str = Field()


bot_settings = BotSettings()
