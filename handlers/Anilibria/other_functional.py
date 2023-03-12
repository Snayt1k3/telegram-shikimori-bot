import aiohttp
from aiogram import types

from misc.constants import ani_url


async def get_torrent(message: types.Message, anime_title):
    pass


async def get_anime_video(message: types.Message, anime_title):
    pass


async def get_anime_info(id_title: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{ani_url}title?id={id_title}') as response:
            return await response.json()
