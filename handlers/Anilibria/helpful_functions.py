import requests
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from anilibria import Title

from bot import dp, anilibria_client
from database.animedb import AnimeDB
from database.database import DataBase
from misc.constants import ANI_URL


async def get_torrent(message: types.Message, id_title: int):
    """in the end, this method send torrent files into chat"""
    anime = await anilibria_client.get_title(id=id_title)
    torr_list = anime.torrents.list

    for torrent in torr_list:
        r = requests.get(url=ANI_URL + torrent.url)
        await message.bot.send_document(
            message.chat.id,
            (f"{anime.names.en}.torrent", r.content),
            caption=f"{torrent.episodes.string} "
            f"{torrent.quality.string} "
            f"{torrent.total_size}",
        )


async def display_edit_message(message: types.Message, kb, anime_info: Title):
    """this method used for edit message, with a photo, if didn't have a photo in message, probably get an error"""
    await message.bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=message.message_id,
        media=types.InputMediaPhoto(ANI_URL + anime_info.posters.small.url),
    )

    await message.bot.edit_message_caption(
        message.chat.id,
        message.message_id,
        reply_markup=kb,
        caption=f"<b>{anime_info.names.ru} | {anime_info.names.en}</b>\n\n"
        f"<b>Год</b>: {anime_info.season.year}\n"
        f"<b>Жанры</b>: {', '.join(anime_info.genres)}\n"
        f"<b>Озвучили</b>: {', '.join(anime_info.team.voice)}",
    )


async def display_search_anime(message: types.Message):
    """this method send a message for search_animes"""
    animes = await AnimeDB.get_anilibria_list(message.chat.id, "anilibria_search")

    kb = InlineKeyboardMarkup()

    for anime in animes[:10]:
        kb.add(
            InlineKeyboardButton(anime.title_ru, callback_data=f"{anime.id}.search_al")
        )

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"cancel.search_al"))

    if len(animes) > 10:
        await message.answer(
            "Не все аниме влезли в список, попробуйте написать по точнее."
        )

    await message.bot.send_photo(
        message.chat.id,
        open("misc/img/pic2.png", "rb"),
        "Нажмите на Интересующее вас Аниме",
        reply_markup=kb,
    )


async def display_anime_which_founds_on_shiki(message: types.Message, animes):
    """
    :param message:
    :param animes: this json response from shikimori
    :return: None
    """
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime["russian"], callback_data=f"view.{anime['id']}.shikimori_founds"
            )
        )

    # make cancel btn
    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"cancel.shikimori_founds"))

    await message.answer(
        "Нажмите на интересующее вас Аниме, \nкоторое было найдено на Shikimori",
        reply_markup=kb,
    )


async def edit_all_follows_markup(message: types.Message, action, page):
    """this method implements pagination with reply_markup"""
    record = await DataBase.find_one("chat_id", message.chat.id, "user_follows")

    if action == "-":
        page -= 8
    else:
        page += 8

    kb = InlineKeyboardMarkup()

    animes = [
        await anilibria_client.get_title(anime)
        for anime in record["animes"][page : page + 8]
    ]

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime.names.ru, callback_data=f"view.{anime.id}.all_follows"
            )
        )

    # add pagination buttons response by current page
    if len(record["animes"]) > page + 8 and page != 0:
        kb.add(
            InlineKeyboardButton(text="<<", callback_data=f"prev.{page}.all_follows"),
            InlineKeyboardButton(text=">>", callback_data=f"next.{page}.all_follows"),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton(text="<<", callback_data=f"prev.{page}.all_follows")
        )
    else:
        kb.add(
            InlineKeyboardButton(text=">>", callback_data=f"next.{page}.all_follows"),
        )

    await dp.bot.edit_message_reply_markup(
        message.chat.id, message.message_id, reply_markup=kb
    )
