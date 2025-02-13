from pydantic import Field

from src.config.base import Settings


class BotSettings(Settings):
    API_TOKEN: str = Field()


bot_settings = BotSettings()
