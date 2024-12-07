import logging

from aiokafka import AIOKafkaConsumer
from src.application.dto.event import EventResponse, Event
from src.application.exception.kafka import UnknownMessageType
from src.application.interfaces.kafka import KafkaAsyncInterface

logger = logging.getLogger(__name__)


class KafkaAsync(KafkaAsyncInterface):
    async def produce(self, topic: str, message: EventResponse) -> None:
        """
        Асинхронная отправка сообщения в Kafka.
        :param topic: Топик, в который отправляется сообщение.
        :param message: Сообщение для отправки.
        """
        raise NotImplementedError

    async def _process_message(self, message: dict) -> None:
        """
        Обрабатывает сообщение, вызывая соответствующий хендлер.
        :param message: Декодированное сообщение.
        """
        data = Event.from_dict(message)
        handler = self.factory_handlers.create(data.event_type)

        if not handler:
            logger.error(f"Unknown message type: {data.event_type}")
            raise UnknownMessageType(f"Unknown message type: {data.event_type}")

        await handler(data)

    async def consume(self, topic: str, group_id: str):
        """
        Асинхронное получение сообщений из Kafka.
        :param topic: Топик для чтения.
        :param group_id: Идентификатор группы консюмера.
        """
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.brokers,
            group_id=group_id,
            auto_offset_reset="earliest",
        )
        await consumer.start()
        try:
            logger.info(f"Sub on topic: {topic}")
            async for msg in consumer:
                logger.info("Processing message")
                await self._process_message(msg.value.decode("utf-8"))
        finally:
            await consumer.stop()
