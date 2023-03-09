import aiohttp
from bot import dp, db_client
from misc.constants import headers


async def check_anime_title(title):
    """Validation Anime Title"""
    async with aiohttp.ClientSession(headers=headers) as session:
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

