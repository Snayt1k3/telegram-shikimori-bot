from pydantic import Field

from src.settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_TOPIC: str = Field()
    GROUP_ID: str = Field()
    RESPONSE_TOPIC: str = Field()
    BROKERS: str = Field()


kafka_settings = KafkaSettings()
