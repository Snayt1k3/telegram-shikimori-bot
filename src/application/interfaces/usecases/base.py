from abc import ABC, abstractmethod


class UseCase(ABC):

    @abstractmethod
    async def __call__(self, **kwargs):
        raise NotImplementedError

