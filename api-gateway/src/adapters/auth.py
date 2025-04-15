import logging
from abc import ABC, abstractmethod

import aiohttp
from fastapi import HTTPException
from pydantic import ValidationError

from src.config.http import http_cfg
from src.dto import AuthenticatedUser, UserGetRequest, UserAuthRequest

logger = logging.getLogger(__name__)


class AbstractAuthService(ABC):

    @abstractmethod
    async def get_uri(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user: UserGetRequest) -> AuthenticatedUser:
        raise NotImplementedError

    @abstractmethod
    async def auth_user(self, user: UserAuthRequest) -> AuthenticatedUser:
        raise NotImplementedError


class AuthService(AbstractAuthService):
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
        return res.get("data", {}).get("uri")

    async def get_user(self, user: UserGetRequest) -> AuthenticatedUser:
        res = await self._request(
            "POST", url=self.base_url + "/check", json={"user_id": user.telegram_id}
        )

        if res["data"] is None:
            raise HTTPException(detail="User not found.", status_code=404)

        return AuthenticatedUser.model_validate(res["data"])

    async def auth_user(self, user: UserAuthRequest) -> AuthenticatedUser:
        res = await self._request(
            "POST",
            url=self.base_url + "/",
            json={"user_id": user.telegram_id, "token": user.token},
        )
        return AuthenticatedUser.model_validate(res["data"])

def get_auth_client() -> AbstractAuthService:
    return AuthService()