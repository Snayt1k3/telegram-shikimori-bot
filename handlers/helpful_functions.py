import aiohttp

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
    def wrapper():
        check_token()
        func()
    return wrapper
