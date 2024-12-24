from abc import ABC, abstractmethod

from src.dto.auth import UserAuthDTO


class BaseAuth(ABC):

    @abstractmethod
    async def get_uri(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def check_user(self, user: UserAuthDTO):
        raise NotImplementedError

    @abstractmethod
    async def auth_user(self, token: str):
        raise NotImplementedError
