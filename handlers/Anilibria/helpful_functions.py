import asyncio

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


async def get_torrent(message: types.Message, id_title: int):
    """in the end, this method send torrent files into chat"""
    anime = await get_anime_info_from_al(id_title)
    torr_list = anime['torrents']['list']

    for torrent in torr_list:
        r = requests.get(url=ani_url + torrent['url'])
        await dp.bot.send_document(message.chat.id, (f"{anime['names']['en']}.torrent", r.content),
                                   caption=f"{torrent['episodes']['string']} "
                                           f"{torrent['quality']['string']} "
                                           f"{torrent['size_string']}")


async def get_anime_info_from_al(id_title) -> dict:
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
                                      parse_mode='HTML',
                                      caption=f"<b>{anime_info['names']['ru']} | {anime_info['names']['en']}</b>\n\n"
                                              f"<b>Год</b>:{anime_info['season']['year']}\n"
                                              f"<b>Жанры</b>: {', '.join(anime_info['genres'])}\n"
                                              f"<b>Озвучили</b>: {', '.join(anime_info['team']['voice'])}",
                                      )


async def display_search_anime(message: types.Message):
    """this method send a message for search_animes"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_search_al']
    record = collection.find_one({'chat_id': message.chat.id})

    kb = InlineKeyboardMarkup()

    for anime_id in record['animes'][:10]:
        anime_info = await get_anime_info_from_al(anime_id)
        kb.add(InlineKeyboardButton(anime_info['names']['ru'], callback_data=f"{anime_id}.search_al"))

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f'cancel.search_al'))

    if len(record['animes']) > 10:
        await message.answer("Не все аниме влезли в список, попробуйте написать по точнее")

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'), "Нажмите на Интересующее вас Аниме",
                            reply_markup=kb)


async def display_anime_which_founds_on_shiki(message: types.Message, animes):
    """
    :param message:
    :param animes: this json response from shikimori
    :return: None
    """
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(InlineKeyboardButton(anime['russian'],
                                    callback_data=f"view.{anime['id']}.shikimori_founds"))

    # make cancel btn
    kb.add(InlineKeyboardButton('❌ Cancel', callback_data=f'cancel.shikimori_founds'))

    await message.answer("Нажмите на Интересующее вас Аниме, \nкоторое было найдено на Shikimori",
                         reply_markup=kb)


async def edit_all_follows_markup(message: types.Message, action, page):
    """this method implements pagination with reply_markup"""
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']
    # check user follow anime exists
    record = collection.find_one({'chat_id': message.chat.id})

    if action == '-':
        page -= 8
    else:
        page += 8

    kb = InlineKeyboardMarkup()
    # get all responses
    tasks = [get_anime_info_from_al(anime_id) for anime_id in record['animes'][page: page + 8]]
    responses = await asyncio.gather(*tasks)

    for anime_info in responses:
        kb.add(InlineKeyboardButton(anime_info['names']['ru'], callback_data=f'view.{anime_info["id"]}.all_follows'))

    # Kb actions
    if len(record['animes']) > page + 8 and page != 0:
        kb.add(
            InlineKeyboardButton(text='<<prev', callback_data=f'prev.{page}.all_follows'),
            InlineKeyboardButton(text='next>>', callback_data=f'next.{page}.all_follows'),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton(text='<<prev', callback_data=f'prev.{page}.all_follows'))
    else:
        kb.add(
            InlineKeyboardButton(text='next>>', callback_data=f'next.{page}.all_follows'),
        )

    await dp.bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=kb)
