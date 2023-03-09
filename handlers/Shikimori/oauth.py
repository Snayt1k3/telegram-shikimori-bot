import os
import aiohttp
from misc.constants import headers

files = {
    'grant_type': (None, 'refresh_token'),
    'client_id': (None, os.environ.get("CLIENT_ID", 'Q0r8QI6H0HrbYEhYwUVpDnEak2_7AmVuuNEX8lHqzuU')),
    'client_secret': (None, os.environ.get("CLIENT_SECRET", 'Ssj4c-XvnA268qk0B_oaf173HrpBEkYiohlscB8m1eQ')),
    'refresh_token': (None, os.environ.get("REFRESH_TOKEN", '3zS5Fh-UhrdLfAoFN589y3ohT_G_iu0WAWzmHlB6raw')),
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
