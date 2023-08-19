import os

import aiohttp

from database.database import DataBase

headers = {"User-Agent": os.environ.get("USER_AGENT")}

files = {
    "grant_type": "refresh_token",
    "client_id": os.environ.get("CLIENT_ID"),
    "client_secret": os.environ.get("CLIENT_SECRET"),
}

shiki_url = "https://shikimori.me/"


async def get_refresh_token(chat_id):
    # get tokens
    record = await DataBase.find_one("chat_id", chat_id, "users_id")

    return record["refresh_token"]


async def get_access_token(chat_id):
    """Token Updater"""
    async with aiohttp.ClientSession(headers=headers) as session:
        files.update({"refresh_token": await get_refresh_token(chat_id)})
        async with session.post(f"{shiki_url}oauth/token", json=files) as response:
            res = await response.json(content_type=None)
            return res


async def check_token(chat_id, token):
    """Token Checker"""
    async with aiohttp.ClientSession(
        headers={
            "User-Agent": os.environ.get("USER_AGENT"),
            "Authorization": "Bearer " + token,
        }
    ) as session:
        async with session.get(f"{shiki_url}api/users/whoami") as response:
            if response.status == 401:
                return await get_access_token(chat_id)
            return None


async def get_first_token(code):
    f_headers = {
        "User-Agent": os.environ.get("USER_AGENT"),
    }

    f_files = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "code": code,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    }

    async with aiohttp.ClientSession(headers=f_headers) as session:
        async with session.post(f"{shiki_url}oauth/token", json=f_files) as response:
            if response.status == 200:
                return await response.json()
            return None
