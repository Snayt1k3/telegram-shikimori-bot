from abc import ABC, abstractmethod
from src.adapters.message_queue import MessageQueueI, KafkaClient
from src.dto.mq import MQMessage
from fastapi import HTTPException
from src.settings.kafka import kafka_settings


class MessageQueueClientI(ABC):
    """
    This class make requests to another service via message queue
    """

    @abstractmethod
    async def send_message_and_wait(self, message: MQMessage) -> dict | None:
        raise NotImplementedError



class MessageQueueClientImpl(MessageQueueClientI):
    def __init__(self, message_queue: MessageQueueI):
        self._mq = message_queue
        self.add_listener(kafka_settings.response_topics)

    @staticmethod
    def _raise_on_error(message: dict) -> None:
        if message.get("error", None):
            raise HTTPException(status_code=message["status_code"], detail=message["error"])
    
    def add_listener(self, topics: list[str]) -> None:
        self._mq.add_listener(topics)

    async def send_message_and_wait(self, topic: str, message: MQMessage) -> dict | None:
        response = await self._mq.send_message(
            topic=topic,
            correlation_id=message.correlation_id,
            message=message.to_dict()
        )

        self._raise_on_error(response)
        return response["data"]


def message_queue_client() -> MessageQueueClientI:
    return MessageQueueClientImpl(KafkaClient(kafka_settings.BROKERS))