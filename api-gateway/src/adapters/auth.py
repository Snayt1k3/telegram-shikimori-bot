import logging
from abc import ABC, abstractmethod

import aiohttp
from fastapi import HTTPException
from src.dto.auth import UserCheckDTO, User, UserAuthDTO
from src.config.http import http_cfg

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
        self.base_url = http_cfg.AUTH_URL

    @staticmethod
    async def _request(method: str, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()

        except aiohttp.ClientResponseError as e:
            raise HTTPException(detail=str(e), status_code=e.status)

        except Exception as e:
            logger.error(f"Error occurred while sending request error={e}")
            raise HTTPException(detail=str(e), status_code=502)

    async def get_uri(self) -> str | None:
        res = await self._request("GET", url=self.base_url + "/uri")
        return res["data"]["uri"]

    async def check_user(self, user: UserCheckDTO) -> User:
        res = await self._request(
            "POST", url=self.base_url + "/check", json={"user_id": user.telegram_id}
        )
        return User(**res["data"])

    async def auth_user(self, user: UserAuthDTO) -> User:
        res = await self._request(
            "POST",
            url=self.base_url + "/",
            json={"user_id": user.telegram_id, "token": user.token},
        )
        return User(**res["data"])
