import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class KafkaAsyncInterface(ABC):

    @abstractmethod
    async def _process_message(self, message: dict, response_topic: str) -> None:
        """
        Обрабатывает сообщение, вызывая соответствующий хендлер.
        :param response_topic: Топик для ответа
        :param message: Декодированное сообщение.
        """
        pass

    @abstractmethod
    async def consume(self, topic: str, group_id: str, response_topic: str):
        """
        Асинхронное получение сообщений из Kafka.
        :param topic: Топик для чтения.
        :param response_topic: Топик для ответа
        :param group_id: Идентификатор группы консюмера.
        """
        pass
