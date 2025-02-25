from pydantic import Field

from src.settings.base import Settings


class KafkaSettings(Settings):
    KAFKA_ANIME_TOPIC: str = Field()
    KAFKA_ANIME_RESPONSE_TOPIC: str = Field()
    GROUP_ID: str = Field()
    BROKERS: str = Field()

    @property
    def response_topics(self) -> list[str]:
        return [self.KAFKA_ANIME_RESPONSE_TOPIC]


kafka_settings = KafkaSettings()
