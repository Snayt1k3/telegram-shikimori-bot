import os

import aiohttp
from misc.constants import SHIKI_URL
from database.repositories.shikimori import shiki_repository
from database.dto import api_client


class ShikiAuth:
    def __init__(self):
        self._files = {
            "grant_type": "refresh_token",
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
        }
        self._headers = api_client.ShikiHeaders(user_agent=os.environ.get("USER_AGENT"))
        self.url = SHIKI_URL

    @staticmethod
    async def _get_refresh_token(chat_id: str | int) -> str:
        """
        getting refresh token from db collection
        """
        record = await shiki_repository.get_one(
            filter={"chat_id": chat_id}, collection="users_id"
        )

        return record["refresh_token"]

    async def _get_access_token(self, chat_id: str | int) -> dict:
        """Token Updater"""
        async with aiohttp.ClientSession(headers=self._headers.to_dict()) as session:
            self._files.update(
                {"refresh_token": await self._get_refresh_token(chat_id)}
            )
            async with session.post(
                f"{self.url}oauth/token", json=self._files
            ) as response:
                return await response.json()

    async def check_token(self, chat_id: str | int, token: str) -> dict | None:
        """
        This func is checking token is valid or not

        :Params:
        - chat_id: Telegram chat id which is uses to identifier user.
        - token: it's token from shikimori

        :returns: None - valid. dict - new token.
        """
        async with aiohttp.ClientSession(
            headers={
                "User-Agent": os.environ.get("USER_AGENT"),
                "Authorization": "Bearer " + token,
            }
        ) as session:
            async with session.get(f"{self.url}api/users/whoami") as response:
                if response.status == 401:
                    return await self._get_access_token(chat_id)
                return None

    async def get_first_token(self, code: str):
        """
        request from shikimori jwt tokens for the first time
        """
        headers = {
            "User-Agent": os.environ.get("USER_AGENT"),
        }
        files = {
            "grant_type": "authorization_code",
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "code": code,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(f"{self.url}oauth/token", json=files) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_headers(self, chat_id) -> api_client.ShikiAuthHeaders:
        """
        this func forming headers, if our request requires auth scope
        """
        record = await shiki_repository.get_one(
            filter={"chat_id": chat_id}, collection="users_id"
        )
        # check user token
        res = await self.check_token(chat_id, record["access_token"])

        if res is not None:
            headers = api_client.ShikiAuthHeaders(
                user_agent=os.environ.get("USER_AGENT"),
                authorization=res["access_token"],
            )

            await shiki_repository.update_tokens(
                chat_id,
                {
                    "access_token": res["access_token"],
                    "refresh_token": res["refresh_token"],
                },
            )
        else:
            headers = api_client.ShikiAuthHeaders(
                user_agent=os.environ.get("USER_AGENT"),
                authorization=record["access_token"],
            )

        return headers


auth = ShikiAuth()
