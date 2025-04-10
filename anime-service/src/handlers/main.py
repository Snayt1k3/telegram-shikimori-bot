import logging

from src.adapters.kafka import KafkaAsync
from src.adapters.storage.models.base import get_session
from src.config.kafka import kafka_cfg
from src.handlers import title, rate, user
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)

handlers = {
    "add_rate": rate.add_rate,
    "read_rates": rate.read_rates,
    "read_titles": title.read_titles,
    "update_rate": rate.update_rate,
    "delete_rate": rate.delete_rate,
    "load_rates": user.load_user,
    "get_profile": user.user_profile,
}


async def start_receiving_messages():
    ioc = IoC(get_session())
    kafka = KafkaAsync(brokers=kafka_cfg.BROKERS, ioc=ioc, handlers=handlers)

    try:
        logger.info("Kafka is running")
        await kafka.consume(
            topic=kafka_cfg.ANIME_TOPIC,
            group_id=kafka_cfg.GROUP_ID,
            response_topic=kafka_cfg.ANIME_RESPONSE_TOPIC,
        )

    except KeyboardInterrupt:
        logger.info("Kafka stopped")

    except Exception as e:
        logger.error(f"Kafka crashed error={e}")
