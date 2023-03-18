import aiohttp
from bot import dp, db_client
from misc.constants import get_headers, shiki_url


async def check_anime_title(title, chat_id):
    """Validation Anime Title"""
    async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
        async with session.get(f"https://shikimori.one/api/animes?search={title}&limit=5") as response:
            anime_founds = await response.json()
            if anime_founds:
                return anime_founds[0]
    return None


async def check_user_in_database(chat_id: int) -> bool:
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["ids_users"]

    if collection.find_one({'chat_id': chat_id}):
        return True

    await dp.bot.send_message(chat_id, 'You need to call command /MyProfile and link your nickname')
    return False


async def check_user_shiki_id(chat_id):
    """Checks that the user has not linked someone else's account"""
    # get db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["ids_users"]
    # get one record
    record = collection.find_one({'chat_id': chat_id})

    async with aiohttp.ClientSession(headers=await get_headers(chat_id)) as session:
        async with session.get(f"{shiki_url}api/users/whoami") as response:
            response = await response.json()

    if record['shikimori_id'] != response['id']:
        collection.update_one({'chat_id': chat_id}, {"$set": {'shikimori_id': response['id']}})



