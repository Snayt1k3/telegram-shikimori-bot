import os

import aiohttp

from database.database import db_repository


class ShikiAuth:
    SHIKI_URL = "https://shikimori.one/"

    def __init__(self):
        self.files = {
            "grant_type": "refresh_token",
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
        }
        self.headers = {"User-Agent": os.environ.get("USER_AGENT")}

    @staticmethod
    async def get_refresh_token(chat_id):
        """
        getting refresh token from db collection
        """
        record = await db_repository.get_one(
            filter={"chat_id": chat_id}, collection="users_id"
        )

        return record["refresh_token"]

    async def get_access_token(self, chat_id):
        """Token Updater"""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            self.files.update({"refresh_token": await self.get_refresh_token(chat_id)})
            async with session.post(f"{SHIKI_URL}oauth/token", json=self.files) as response:
                res = await response.json(content_type=None)
                return res

    async def check_token(self, chat_id, token):
        """Token Checker"""
        async with aiohttp.ClientSession(
                headers={
                    "User-Agent": os.environ.get("USER_AGENT"),
                    "Authorization": "Bearer " + token,
                }
        ) as session:
            async with session.get(f"{self.SHIKI_URL}api/users/whoami") as response:
                if response.status == 401:
                    return await self.get_access_token(chat_id)
                return None

    async def get_first_token(self, code):
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
            async with session.post(f"{self.SHIKI_URL}oauth/token", json=files) as response:
                if response.status == 200:
                    return await response.json()
                return None

    @staticmethod
    async def get_headers(chat_id) -> dict:
        """This method implements OAuth on shikimori"""
        record = await db_repository.get_one(
            filter={"chat_id": chat_id}, collection="users_id"
        )
        # check user token
        res = await check_token(chat_id, record["access_token"])

        if res is not None:
            headers = {
                "User-Agent": os.environ.get("USER_AGENT"),
                "Authorization": "Bearer " + res["access_token"],
            }

            # update user token
            await db_repository.update_one(
                "users_id",
                {
                    "chat_id": chat_id,
                },
                {
                    "access_token": res["access_token"],
                    "refresh_token": res["refresh_token"],
                },
            )
        else:
            headers = {
                "User-Agent": os.environ.get("USER_AGENT"),
                "Authorization": "Bearer " + record["access_token"],
            }

        return headers


auth = ShikiAuth()
