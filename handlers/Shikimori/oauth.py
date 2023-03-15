import os
import aiohttp
from misc.constants import get_headers
headers = {
    'User-Agent': "Snayt1k3-API"
}

files = {
    'grant_type': 'refresh_token',
    'client_id': os.environ.get("CLIENT_ID"),
    'client_secret': os.environ.get("CLIENT_SECRET"),
    'refresh_token': os.environ.get("REFRESH_TOKEN"),
}


async def get_access_token():
    """Token Updater"""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"https://shikimori.one/oauth/token", json=files) as response:
            res = await response.json()
            os.environ["ACCESS_TOKEN"] = res['access_token']
            os.environ["REFRESH_TOKEN"] = res['refresh_token']


async def check_token():
    """Token Checker"""
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(f"https://shikimori.one/api/users/whoami") as response:
            if response.status == 401:
                await get_access_token()
