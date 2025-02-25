import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logger = logging.getLogger(__name__)


class MessageQueueI(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def send_message(
        self, topic: str, message: dict, correlation_id: str
    ) -> dict:
        pass

    @abstractmethod
    def add_listener(self, topics: List[str]):
        pass


class KafkaClient(MessageQueueI):
    def __init__(self, brokers: str):
        """
        Инициализация Kafka-клиента.
        :param brokers: Адреса брокеров Kafka.
        """
        self.brokers = brokers
        self._producer: Optional[AIOKafkaProducer] = None
        self._response_futures: Dict[str, asyncio.Future] = {}
        self._listeners = []

    async def start(self):
        """
        Инициализация Kafka-продюсера.
        """
        if not self._producer:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()
            logger.info("Kafka producer started")

    async def stop(self):
        """
        Остановка Kafka-продюсера и всех слушателей.
        """
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped")

        # Остановка всех задач для прослушивания
        for listener in self._listeners:
            listener.cancel()

    async def send_message(
        self, topic: str, message: dict, correlation_id: str
    ) -> dict:
        """
        Отправляет сообщение в Kafka и ожидает ответа.
        :param topic: Топик для отправки.
        :param message: Сообщение для отправки.
        :param correlation_id: Уникальный идентификатор сообщения.
        :return: Ответ из Kafka.
        """
        await self.start()
        future = asyncio.Future()
        self._response_futures[correlation_id] = future

        try:
            logger.info(f"Sending message to topic: {topic}")
            await self._producer.send_and_wait(
                topic,
                value=json.dumps(message).encode("utf-8"),
                key=correlation_id.encode("utf-8"),
            )
            return await asyncio.wait_for(future, timeout=10)
        except asyncio.TimeoutError:
            logger.error(f"Timeout waiting for response to {correlation_id}")
            return {"error": "Something went wrong. Try again", "status_code": 504}
        finally:
            self._response_futures.pop(correlation_id, None, None)

    async def listen_responses(self, topics: List[str]):
        """
        Слушает ответы из Kafka с нескольких топиков.
        :param topics: Список топиков для прослушивания.
        """
        consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.brokers,
            auto_offset_reset="earliest",
        )
        await consumer.start()
        try:
            logger.info(f"Subscribed to response topics: {topics}")
            async for msg in consumer:
                try:
                    correlation_id = msg.key.decode("utf-8")
                    response_data = json.loads(msg.value.decode("utf-8"))
                    logger.info(
                        f"Received response for {correlation_id} from topic {msg.topic}: {response_data}"
                    )

                    if correlation_id in self._response_futures:
                        self._response_futures[correlation_id].set_result(response_data)
                except Exception as e:
                    logger.error(
                        f"Error processing response message: {e}", exc_info=True
                    )
        finally:
            await consumer.stop()

    def add_listener(self, topics: List[str]):
        """
        Добавляет задачу для прослушивания нескольких топиков.
        :param topics: Список топиков.
        """
        task = asyncio.create_task(self.listen_responses(topics))
        self._listeners.append(task)
