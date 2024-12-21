import logging

from src.adapters.kafka import KafkaAsync
from src.handlers.ioc import IoC
from src.adapters.storage.models.base import get_session

logger = logging.getLogger(__name__)

handlers = {}


async def start_receiving_messages():
    ioc = IoC(get_session())  # dependency container
    kafka = KafkaAsync()  # todo Настройка

    try:
        logger.info("Kafka is running")
        await kafka.consume()  # todo Настройка

    except KeyboardInterrupt:
        logger.info("Kafka stopped")

    except Exception as e:
        logger.error(f"Kafka crashed error={e}")
