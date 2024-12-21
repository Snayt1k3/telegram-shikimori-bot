import logging
from abc import ABC, abstractmethod
from typing import Callable, Any

from src.application.dto.event import Event

logger = logging.getLogger(__name__)


class KafkaAsyncInterface(ABC):
    @abstractmethod
    def register_handler(
        self, event_type: str, handler: Callable[[Event], Any]
    ) -> None:
        """
        Регистрирует хендлер для указанного типа события.
        :param event_type: Тип события (например, "user.created").
        :param handler: Функция для обработки события.
        """
        pass

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
