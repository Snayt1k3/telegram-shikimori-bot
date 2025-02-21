from abc import abstractmethod, ABC
from src.adapters.http import BaseHttpAdapter
from typing import TypedDict
from src.config.http import http_settings


class UserResponse(TypedDict):
    id: int
    shikimori_id: int
    token: str


class BaseAuthAdapter(ABC):
    @abstractmethod
    async def get_uri(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, id_telegram: int) -> UserResponse | None:
        raise NotImplementedError

    @abstractmethod
    async def auth_user(self, id_telegram: int, code: str) -> UserResponse | None:
        raise NotImplementedError


class AuthAdapter(BaseAuthAdapter):
    def __init__(self, request: BaseHttpAdapter):
        self._request = request

    async def get_uri(self) -> str | None:
        response = await self._request.get(http_settings.AUTH_URL + "/uri")
        return response["data"].get("uri", "")

    async def get_user(self, id_telegram: int) -> UserResponse | None:
        response = await self._request.post(
            http_settings.AUTH_URL + "/check", json={"user_id": id_telegram}
        )

        return response["data"]

    async def auth_user(self, id_telegram: int, code: str) -> UserResponse | None:
        response = await self._request.post(
            http_settings.AUTH_URL, json={"user_id": id_telegram, "token": code}
        )

        return response["data"]
