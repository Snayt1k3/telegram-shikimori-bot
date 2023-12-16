import abc
import logging

from database.dto import api_client
import aiohttp


class BaseApiClient(abc.ABC):
    async def get(
        self, url: str, query_params: dict = None, headers: dict = None
    ) -> api_client.BaseResponse:
        """
        make a get request to url

        Params:
            - url(str): url, which we make a request.
            - query_params(dict): params.
            - headers(dict): headers of request.

        Returns: obj of dto Response

        """
        return await self._get(url, query_params, headers)

    @abc.abstractmethod
    async def _get(
        self, url: str, query_params: dict, headers: dict
    ) -> api_client.BaseResponse:
        raise NotImplementedError

    async def post(
        self, url: str, body: dict, headers: dict
    ) -> api_client.BaseResponse:
        """
        make a post request to url

        Params:
            - url(str): url, which we make a request.
            - body(dict): body of request.
            - headers(dict): headers of request.

        Returns: obj of dto Response
        """
        return await self._post(url, body, headers)

    @abc.abstractmethod
    async def _post(
        self, url: str, body: dict, headers: dict
    ) -> api_client.BaseResponse:
        raise NotImplementedError

    async def patch(
        self, url: str, body: dict, headers: dict
    ) -> api_client.BaseResponse:
        """
        make a patch request to url

        Params:
            - url(str): url, which we make a request.
            - body(dict): body of request.
            - headers(dict): headers of request.

        Returns: obj of dto Response
        """
        return await self._patch(url, body, headers)

    @abc.abstractmethod
    async def _patch(self, url: str, body: dict, headers: dict):
        raise NotImplementedError


class ApiClient(BaseApiClient):
    async def _get(
        self, url: str, query_params: dict, headers: dict
    ) -> api_client.BaseResponse:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, params=query_params) as response:
                    response.raise_for_status()

                    return api_client.BaseResponse(
                        status=response.status, text=await response.json()
                    )

        except aiohttp.ClientResponseError as e:
            logging.error(
                f"Bad request in ApiClient(get). status - {e.status}, message - {e.message}"
            )
            return api_client.BaseResponse(status=e.status, text={})

        except Exception as e:
            logging.error(f"Error occurred in ApiClient(get) - {e}")
            return api_client.BaseResponse(status=e.status, text={})

    async def _post(
        self, url: str, body: dict, headers: dict
    ) -> api_client.BaseResponse:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=body) as response:
                    response.raise_for_status()

                    return api_client.BaseResponse(
                        status=response.status, text=await response.json()
                    )

        except aiohttp.ClientResponseError as e:
            logging.error(
                f"Bad request in ApiClient(post). status - {e.status}, message - {e.message}"
            )
            return api_client.BaseResponse(status=e.status, text={})

        except Exception as e:
            logging.error(f"Error occurred in ApiClient(post) - {e}")
            return api_client.BaseResponse(status=e.status, text={})

    async def _patch(
        self, url: str, body: dict, headers: dict
    ) -> api_client.BaseResponse:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=body) as response:
                    response.raise_for_status()

                    return api_client.BaseResponse(
                        status=response.status, text=await response.json()
                    )

        except aiohttp.ClientResponseError as e:
            logging.error(
                f"Bad request in ApiClient(patch). status - {e.status}, message - {e.message}"
            )
            return api_client.BaseResponse(status=e.status, text={})

        except Exception as e:
            logging.error(f"Error occurred in ApiClient(patch) - {e}")
            return api_client.BaseResponse(status=e.status, text={})
