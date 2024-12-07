from abc import ABC, abstractmethod


class UseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        raise NotImplementedError
