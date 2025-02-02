import abc
import logging
from typing import Literal, TypedDict
import aiohttp

logger = logging.getLogger(__name__)


class ResponseDTO(TypedDict):
    data: dict | list | None
    error: str | None
    status: int


class BaseHttpAdapter(abc.ABC):
    @abc.abstractmethod
    async def post(self, url: str, **kwargs) -> ResponseDTO:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, url: str, **kwargs) -> ResponseDTO:
        raise NotImplementedError

    @abc.abstractmethod
    async def patch(self, url: str, **kwargs) -> ResponseDTO:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, url, **kwargs) -> ResponseDTO:
        raise NotImplementedError


class HttpAdapter(BaseHttpAdapter):
    @staticmethod
    async def _request(
        method: Literal["POST", "PATCH", "GET", "DELETE"], url: str, **kwargs
    ):
        try:

            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()

        except aiohttp.ClientResponseError as e:
            logger.error(
                f"Bad response for url={url}, status={e.status}, message={e.message}"
            )

        except Exception as e:
            logger.error(f"Something went wrong, {e}")

        return {}

    async def get(self, url: str, **kwargs) -> ResponseDTO:
        return await self._request("GET", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> ResponseDTO:
        return await self._request("PATCH", url, **kwargs)

    async def delete(self, url, **kwargs) -> ResponseDTO:
        return await self._request("DELETE", url, **kwargs)

    async def post(self, url: str, **kwargs) -> ResponseDTO:
        return await self._request("POST", url, **kwargs)
