import aiohttp
from .oauth import check_token
from bot import db_client
from constants import headers, shiki_url


async def get_information_from_anime(anime_id: int) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{shiki_url}api/animes/{anime_id}") as response:
            if response.status == 200:
                return await response.json()


async def get_user_id(chat_id: int) -> int:
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["ids_users"]
    return collection.find_one({'chat_id': chat_id})['shikimori_id']


def oauth2_decorator(func):
    """Decorator for func"""
    async def wrapper(*args, **kwargs):
        await check_token()
        return await func(*args, **kwargs)
    return wrapper


def oauth2_state(func):
    """Decorator for func with state"""
    async def wrapper(*args, **kwargs):
        await check_token()
        return await func(*args, state=kwargs['state'])
    return wrapper


async def check_anime_already_in_planned(chat_id: int, anime_id: int) -> bool:
    id_user = await get_user_id(chat_id)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{shiki_url}api/v2/user_rates?user_id={id_user}&target_id={anime_id}&target_type=Anime") as response:
            json_file = await response.json()
            if json_file:
                return True
            return False
