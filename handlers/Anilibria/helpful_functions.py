import aiohttp
import requests
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import dp, db_client
from misc.constants import ani_api_url, ani_url


async def search_on_anilibria(anime_title: str) -> [dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(ani_api_url + f'title/search?search={anime_title}') as response:
            return await response.json()


async def when_released_anime():
    pass


async def get_torrent(message: types.Message, id_title: int):
    """in the end, this method send torrent files into chat"""
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


async def get_anime_info(id_title: int) -> dict:
    """Make a request to anilibria.api, Collect info from a Specifically title"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{ani_api_url}title?id={id_title}') as response:
            return await response.json()


async def display_edit_message(message: types.Message, kb, anime_info: dict):
    """this method used for edit message, with a photo, if didn't have a photo in message, probably error"""
    # edit photo
    await dp.bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id,
                                    media=types.InputMediaPhoto(ani_url + anime_info['posters']['small']['url']),
                                    )

    # edit caption
    await dp.bot.edit_message_caption(message.chat.id, message.message_id,
                                      reply_markup=kb,
                                      caption=f"Название: {anime_info['names']['ru']}\n"
                                              f"Жанры: {', '.join(anime_info['genres'])}\n"
                                              f"Озвучили: {', '.join(anime_info['team']['voice'])}",
                                      )


async def display_search_anime(message: types.Message):
    """this method send a message for search_animes"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_search_al']
    record = collection.find_one({'chat_id': message.chat.id})

    kb = InlineKeyboardMarkup()

    for anime_id in record['animes'][:10]:
        anime_info = await get_anime_info(anime_id)
        kb.add(InlineKeyboardButton(anime_info['names']['en'], callback_data=f"{anime_id}.search_al"))

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f'cancel.search_al'))

    if len(record['animes']) > 10:
        await message.answer("Не все аниме влезли в список, попробуйте написать по точнее")

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'), "Нажмите на Интересующее вас Аниме",
                            reply_markup=kb)
