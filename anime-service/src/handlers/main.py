import logging

from src.adapters.kafka import KafkaAsync
from src.handlers.ioc import IoC
from src.adapters.storage.models.base import get_session
from src.settings.kafka import kafka_settings
from src.handlers import title, rate

logger = logging.getLogger(__name__)

handlers = {
    "read_rate": rate.read_rate,
    "delete_rates": rate.delete_rates,
    "delete_rate": rate.delete_rate,
    "update_rate": rate.update_rate,
    "update_rates": rate.update_rates,
    "read_rates": rate.read_rates,
    "add_rate": rate.add_rate,
    "add_rates": rate.add_rates,
    "read_title": title.read_title,
    "read_titles": title.read_titles,
}


async def start_receiving_messages():
    ioc = IoC(get_session())  # dependency container
    kafka = KafkaAsync(brokers=kafka_settings.BROKERS, ioc=ioc)

    try:
        logger.info("Kafka is running")
        await kafka.consume(
            topic=kafka_settings.ANIME_TOPIC,
            group_id=kafka_settings.GROUP_ID,
            response_topic=kafka_settings.ANIME_RESPONSE_TOPIC,
        )

    except KeyboardInterrupt:
        logger.info("Kafka stopped")

    except Exception as e:
        logger.error(f"Kafka crashed error={e}")
