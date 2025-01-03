import logging
from abc import ABC, abstractmethod

import aiohttp

from src.dto.auth import UserCheckDTO, User, UserAuthDTO

logger = logging.getLogger(__name__)


class BaseAuth(ABC):

    @abstractmethod
    async def get_uri(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def check_user(self, user: UserCheckDTO) -> User:
        raise NotImplementedError

    @abstractmethod
    async def auth_user(self, user: UserAuthDTO) -> User:
        raise NotImplementedError


class AuthImpl(BaseAuth):
    def __init__(self):
        self.base_url = ""

    @staticmethod
    async def _request(method: str, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

    async def get_uri(self) -> str | None:
        try:
            res = await self._request("POST", url=self.base_url + "/uri")
            return res["data"]["uri"]
        except Exception as e:
            logger.error(f"Error occurred while getting uri error={e}")

    async def check_user(self, user: UserCheckDTO) -> User:
        try:
            res = await self._request(
                "POST", url=self.base_url + "/check", json={"user_id": user.id}
            )
            return User(**res["data"])
        except Exception as e:
            logger.error(f"Error occurred while getting uri error={e}")

    async def auth_user(self, user: UserAuthDTO) -> User:
        try:
            res = await self._request(
                "POST",
                url=self.base_url + "/",
                json={"user_id": user.id, "token": user.token},
            )
            return User(**res["data"])
        except Exception as e:
            logger.error(f"Error occurred while getting uri error={e}")
