import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import HTTPException

from src.config import kafka_cfg
from src.dto import MQMessage

logger = logging.getLogger(__name__)


class AbstractMessageQueue(ABC):
    @abstractmethod
    async def _start_producer(self):
        raise NotImplementedError

    @abstractmethod
    async def _stop_producer(self):
        raise NotImplementedError

    @abstractmethod
    async def _send_message(
            self, topic: str, message: dict, correlation_id: str
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    def add_listener(self, topics: List[str]):
        raise NotImplementedError

    @abstractmethod
    async def send_message_and_wait(
            self, topic: str, message: MQMessage
    ) -> dict | None:
        raise NotImplementedError

class KafkaClient(AbstractMessageQueue):
    def __init__(self):
        self.brokers = kafka_cfg.BROKERS
        self._producer: Optional[AIOKafkaProducer] = None
        self._response_futures: Dict[str, asyncio.Future] = {}
        self._listeners = []

    async def _start_producer(self):
        """
        Инициализация Kafka-продюсера.
        """
        if not self._producer:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.brokers)
            await self._producer.start()
            logger.info("Kafka producer started")

    async def _stop_producer(self):
        """
        Остановка Kafka-продюсера и всех слушателей.
        """
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped")

        for listener in self._listeners:
            listener.cancel()

    @staticmethod
    def _raise_on_error(message: dict) -> None:
        if message.get("error", None):
            raise HTTPException(
                status_code=message["status_code"], detail=message["error"]
            )

    async def _send_message(
            self, topic: str, message: dict, correlation_id: str
    ) -> dict:  # type: ignore
        """
        Отправляет сообщение в Kafka и ожидает ответа.
        :param topic: Топик для отправки.
        :param message: Сообщение для отправки.
        :param correlation_id: Уникальный идентификатор сообщения.
        :return: Ответ из Kafka.
        """
        await self._start_producer()
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
            return {"error": "Timeout waiting for response", "status_code": 504}

        except Exception as e:
            logger.exception(f"Error sending message to Kafka: {e}")
            return {"error": "Internal server error", "status_code": 500}

        finally:
            future = self._response_futures.pop(correlation_id, None)
            if future and not future.done():
                future.set_exception(asyncio.TimeoutError("Response timed out"))

    async def _listen_responses(self, topics: List[str]):
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
                    response_data = json.loads(msg.value.decode("utf-8"))
                    correlation_id = response_data.get("correlation_id", "")
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

    async def send_message_and_wait(
            self, topic: str, message: MQMessage
    ) -> dict | None:
        self.add_listener(kafka_cfg.response_topics)
        response = await self._send_message(
            topic=topic,
            correlation_id=str(message.correlation_id),
            message=message.to_dict(),
        )

        self._raise_on_error(response)
        return response["data"]

    def add_listener(self, topics: List[str]) -> None:
        task = asyncio.create_task(self._listen_responses(topics))
        self._listeners.append(task)


def message_queue_client() -> AbstractMessageQueue:
    return KafkaClient()
