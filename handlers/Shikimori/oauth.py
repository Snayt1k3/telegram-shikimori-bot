import os
import aiohttp
from misc.constants import headers

files = {
    'grant_type': (None, 'refresh_token'),
    'client_id': (None, os.environ.get("CLIENT_ID")),
    'client_secret': (None, os.environ.get("CLIENT_SECRET")),
    'refresh_token': (None, os.environ.get("REFRESH_TOKEN")),
}


async def get_access_token():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"https://shikimori.one/oauth/token", data=files) as response:
            res = await response.json()
            os.environ["ACCESS_TOKEN"] = res['access_token']
            os.environ["REFRESH_TOKEN"] = res['refresh_token']


async def check_token():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/users/whoami") as response:
            if response.status == 401:
                await get_access_token()
