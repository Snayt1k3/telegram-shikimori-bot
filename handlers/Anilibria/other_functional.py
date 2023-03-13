import requests
import aiohttp
from aiogram import types

from Keyboard.inline import anilibria_follow_kb
from bot import dp, db_client
from misc.constants import ani_api_url, ani_url


async def get_torrent(message: types.Message, id_title: int):
    anime = await get_anime_info(id_title)
    torr_list = anime['torrents']['list']

    for torrent in torr_list:
        r = requests.get(url=ani_url + torrent['url'])
        await dp.bot.send_document(message.chat.id, (f"{anime['names']['en']}.torrent", r.content),
                                   caption=f"{torrent['episodes']['string']} "
                                           f"{torrent['quality']['string']} "
                                           f"{torrent['size_string']}")


async def get_anime_video(message: types.Message, id_title):
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
    if not record['animes']:
        return

    record = record['animes'][record['page']]

    # kb
    if coll == 'anime_follow_search':
        kb = anilibria_follow_kb
    else:
        kb = None

    # send msg
    await dp.bot.send_photo(chat_id=message.chat.id, photo=ani_url + record['posters']['small']['url'],
                            reply_markup=kb,
                            caption=f"Название: {record['names']['ru']}\n"
                                    f"Жанры: {', '.join(record['genres'])}\n"
                                    f"Озвучили: {', '.join(record['team']['voice'])}")


async def edit_anime_al(message: types.Message, coll: str):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]

    # get datas
    record = collection.find_one({'chat_id': message.chat.id})
    record = record['animes'][record['page']]

    # kb
    if coll == 'anime_follow_search':
        kb = anilibria_follow_kb
    else:
        kb = None

    # edit photo
    await dp.bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id,
                                    media=types.InputMediaPhoto(ani_url + record['posters']['small']['url']),
                                    )

    # edit caption
    await dp.bot.edit_message_caption(message.chat.id, message.message_id,
                                      reply_markup=kb,
                                      caption=f"Название: {record['names']['ru']}\n"
                                              f"Жанры: {', '.join(record['genres'])}\n"
                                              f"Озвучили: {', '.join(record['team']['voice'])}",
                                      )
