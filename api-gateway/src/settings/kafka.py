from pydantic import Field

from src.settings.base import Settings


class KafkaSettings(Settings):
    ANIME_TOPIC: str = Field()
    ANIME_RESPONSE_TOPIC: str = Field()
    GROUP_ID: str = Field()
    BROKERS: str = Field()

    @property
    def response_topics(self) -> list[str]:
        return [self.ANIME_RESPONSE_TOPIC]


kafka_settings = KafkaSettings()
