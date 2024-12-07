from abc import ABC, abstractmethod

from src.application.dto.event import EventResponse
from src.application.interfaces.factory import UseCaseFactoryAbstract


class KafkaAsyncInterface(ABC):
    def __init__(self, brokers, factory: UseCaseFactoryAbstract):
        """
        Инициализация KafkaAsyncInterface.
        :param brokers: Список Kafka брокеров (например, "localhost:9092").
        """
        self.brokers = brokers
        self.factory_handlers = factory

    @abstractmethod
    async def produce(self, topic: str, message: EventResponse) -> None:
        """
        Асинхронная отправка сообщения в Kafka.
        :param topic: Топик, в который отправляется сообщение.
        :param message: Сообщение для отправки.
        """
        raise NotImplementedError

    @abstractmethod
    async def consume(self, topic: str, group_id: str):
        """
        Асинхронное получение сообщений из Kafka.
        :param topic: Топик для чтения.
        :param group_id: Идентификатор группы консюмера.
        """
        raise NotImplementedError
