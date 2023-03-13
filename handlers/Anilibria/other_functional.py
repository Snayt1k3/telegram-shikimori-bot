import aiohttp
from aiogram import types
from bot import dp, db_client
from misc.constants import ani_api_url, ani_url


async def get_torrent(message: types.Message, anime_title):
    pass


async def get_anime_video(message: types.Message, anime_title):
    pass


async def get_anime_info(id_title: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{ani_api_url}title?id={id_title}') as response:
            return await response.json()


async def display_anime_al(message: types.Message, coll: str):
    """this method implements display any list is anime, if right build"""
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]

    # get datas
    record = collection.find_one({'chat_id': message.chat.id})
    record = record['animes'][record['page']]

    # send msg
    await dp.bot.send_photo(chat_id=message.chat.id, photo=ani_url + record['posters']['small']['url'],
                            caption=f"Название: {record['names']['ru']}\n"
                                    f"Жанры: {', '.join(record['genres'])}\n"
                                    f"Озвучили: {', '.join(record['team']['voice'])}")
