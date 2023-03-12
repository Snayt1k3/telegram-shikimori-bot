import json

import aiohttp

from misc.constants import ani_url


async def search_on_anilibria(anime_title: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(ani_url + f'title/search?search={anime_title}') as response:
            return await response.json()


async def when_released_anime():
    pass
