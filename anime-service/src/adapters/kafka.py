import logging
from typing import Callable, Dict, Any, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.application.dto.event import Event, EventResponse
from src.application.dto.response import ResponseDTO
from src.application.exception.kafka import UnknownMessageType
from src.application.interfaces.kafka import KafkaAsyncInterface

logger = logging.getLogger(__name__)


class KafkaAsync(KafkaAsyncInterface):
    def __init__(self, brokers: str):
        """
        Инициализация KafkaAsync с указанными брокерами.
        :param brokers: Адреса брокеров Kafka.
        """
        self.brokers = brokers
        self._handlers: Dict[str, Callable[[Event], Any]] = {}
        self._producer: Optional[AIOKafkaProducer] = None

    async def start_producer(self):
        """
        Инициализация Kafka-продюсера.
        """
        if not self._producer:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()
            logger.info("Kafka producer started")

    async def stop_producer(self):
        """
        Остановка Kafka-продюсера.
        """
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped")

    def register_handler(
        self, event_type: str, handler: Callable[[Event], ResponseDTO]
    ) -> None:
        """
        Регистрирует хендлер для указанного типа события.
        :param event_type: Тип события (например, "user.created").
        :param handler: Функция для обработки события.
        """
        if event_type in self._handlers:
            logger.warning(
                f"Handler for event '{event_type}' is already registered. Overwriting."
            )
        self._handlers[event_type] = handler
        logger.info(f"Handler registered for event type: {event_type}")

    async def _send_response(self, topic: str, response: EventResponse) -> None:
        """
        Отправляет ответ обратно в Kafka.
        :param topic: Топик для отправки.
        :param response: Ответ от обработчика.
        """
        if not self._producer:
            logger.error("Kafka producer is not initialized. Cannot send message.")
            return

        try:
            await self._producer.send_and_wait(topic, value=response)
            logger.info(f"Response sent to topic '{topic}': {response}")
        except Exception as e:
            logger.error(f"Failed to send response: {e}", exc_info=True)

    async def _process_message(self, message: dict, response_topic: str) -> None:
        """
        Обрабатывает сообщение, вызывая соответствующий хендлер, и отправляет ответ.
        :param message: Декодированное сообщение.
        :param response_topic: Топик для отправки ответа.
        """
        try:
            data = Event.from_dict(message)
            event_type = data.event_type

            if event_type not in self._handlers:
                logger.error(f"Unknown message type: {event_type}")
                raise UnknownMessageType(f"Unknown message type: {event_type}")

            handler = self._handlers[event_type]
            logger.info(f"Processing event type: {event_type}")
            response = await handler(data)

            if response_topic:
                await self._send_response(
                    response_topic,
                    EventResponse(
                        data=response["data"],
                        error=response["error"],
                        correlation_id=data.correlation_id,
                        status_code=response["status"],
                    ),
                )

        except Exception as e:
            logger.error(
                f"Failed to process message: {message}, error: {e}", exc_info=True
            )

            await self._send_response(
                response_topic,
                EventResponse(
                    data={},
                    error=str(e),
                    correlation_id=data.correlation_id,
                    status_code=500,
                ),
            )

    async def consume(self, topic: str, group_id: str, response_topic: str):
        """
        Асинхронное получение сообщений из Kafka.
        :param topic: Топик для чтения.
        :param group_id: Идентификатор группы консюмера.
        :param response_topic: Топик для отправки ответа.
        """
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.brokers,
            group_id=group_id,
            auto_offset_reset="earliest",
        )
        await consumer.start()
        await self.start_producer()
        try:
            logger.info(f"Subscribed to topic: {topic}")
            async for msg in consumer:
                logger.info("Received message")
                try:
                    decoded_msg = msg.value.decode("utf-8")
                    await self._process_message(decoded_msg, response_topic)
                except Exception as e:
                    logger.error(f"Error decoding message: {e}", exc_info=True)
        finally:
            logger.info("Stopping Kafka consumer and producer")
            await consumer.stop()
            await self.stop_producer()
