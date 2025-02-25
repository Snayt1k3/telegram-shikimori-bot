from pydantic import Field

from src.settings.base import Settings


class KafkaSettings(Settings):
    ANIME_TOPIC: str = Field()
    GROUP_ID: str = Field()
    ANIME_RESPONSE_TOPIC: str = Field()
    BROKERS: str = Field()


kafka_settings = KafkaSettings()
