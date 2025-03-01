from pydantic import Field

from src.config.base import BaseConfig


class KafkaConfig(BaseConfig):
    ANIME_TOPIC: str = Field()
    GROUP_ID: str = Field()
    ANIME_RESPONSE_TOPIC: str = Field()
    BROKERS: str = Field()


kafka_cfg = KafkaConfig()
