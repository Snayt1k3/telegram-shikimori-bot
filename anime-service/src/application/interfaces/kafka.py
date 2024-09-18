import abc


class AbstractKafkaProducer(abc.ABC):
    def __init__(self, brokers: str):
        self.brokers = brokers
        self.producer = None

    @abc.abstractmethod
    async def start(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def send_message(self, topic: str, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def stop(self):
        raise NotImplementedError


class AbstractKafkaConsumer(abc.ABC):
    def __init__(self, topic: str, brokers: str, group_id: str):
        self.brokers = brokers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None

    @abc.abstractmethod
    async def start(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def consume_messages(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def stop(self):
        raise NotImplementedError
