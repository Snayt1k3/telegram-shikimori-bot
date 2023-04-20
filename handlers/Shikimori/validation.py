import aiohttp
from bot import dp
from misc.constants import get_headers, shiki_url
from database.database import DataBase

async def check_anime_title(title, chat_id):
    """Validation Anime Title"""
    async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
        async with session.get(f"{shiki_url}api/animes?search={title}&limit=5") as response:
            anime_founds = await response.json()
            if anime_founds:
                return anime_founds[0]
    return None


async def check_user_in_database(chat_id: int) -> bool:
    # DB actions
    db = DataBase()

    if db.find_one('chat_id', chat_id, 'ids_users'):
        return True

    await dp.bot.send_message(chat_id, 'You need to call command /MyProfile and link your nickname')
    return False


async def check_user_shiki_id(chat_id):
    """Checks that the user has not linked someone else's account"""
    # get db
    db = DataBase()
    record = db.find_one('chat_id', chat_id, 'ids_users')

    async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
        async with session.get(f"{shiki_url}api/users/whoami") as response:
            response = await response.json()

    if record['shikimori_id'] != response['id']:
        db.update_one('ids_users', 'chat_id', chat_id, {'shikimori_id': response['id']})



