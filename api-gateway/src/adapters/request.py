from abc import ABC, abstractmethod

from src.adapters.kafka import AbstractKafka
from src.dto.mq import MQMessage


class RequestInterface(ABC):
    """
    This class make requests to another service via message queue
    """

    def __init__(self, mq: AbstractKafka) -> None:
        self.mq = mq

    @abstractmethod
    async def send_message_and_wait(self, message: MQMessage) -> dict | None:
        raise NotImplementedError
