import requests
from aiogram import types
from anilibria import Title

from bot import dp, anilibria_client
from database.repositories.anilibria import anilibria_repository
from handlers.Anilibria.keyboards import inline
from handlers.Shikimori.utils.shiki_api import shiki_api
from misc.constants import ANI_URL, SHIKI_URL
from utils.message import message_work


async def get_torrent(message: types.Message, id_title: int):
    """in the end, this method send torrent files into chat"""
    anime = await anilibria_client.get_title(id=id_title)
    torr_list = anime.torrents.list

    for torrent in torr_list:
        r = requests.get(url=ANI_URL + torrent.url)
        await message.reply_document(
            (f"{anime.names.en}.torrent", r.content),
            caption=f"{torrent.episodes.string} "
            f"{torrent.quality.string} "
            f"{torrent.total_size}",
            reply=False,
        )


async def shiki_mark_message(msg: types.Message, id_title: str | int):
    """
    edit msg, for view an anime from shikimori for mark
    """

    anime_info = await shiki_api.get_anime(id_title)
    msg_kb = await inline.shikimori_mark_actions_kb(anime_info["id"])
    msg_text = await message_work.anime_info_msg(anime_info)

    await msg.edit_media(
        types.InputMediaPhoto(SHIKI_URL + anime_info["image"]["original"])
    )
    await msg.edit_caption(msg_text, reply_markup=msg_kb)


async def edit_message_by_title(message: types.Message, kb, anime_info: Title):
    """this method used for edit message, with a photo, if didn't have a photo in message, probably get an error"""
    await message.bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=message.message_id,
        media=types.InputMediaPhoto(anime_info.posters.small.full_url),
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


async def search_anime_msg(message: types.Message):
    """send msg into chat, contains animes which was found on shikimori"""
    animes = await anilibria_repository.get_anilibria_list(
        message.chat.id, "anilibria_search"
    )

    if len(animes) > 10:
        await message.answer(
            "Не все аниме влезли в список, попробуйте написать по точнее."
        )

    kb = await inline.search_anime_kb(animes[:10])

    await message.bot.send_photo(
        message.chat.id,
        open("misc/img/pic2.png", "rb"),
        "Нажмите на Интересующее вас Аниме",
        reply_markup=kb,
    )


async def anime_from_shikimori_msg(message: types.Message, animes: list[dict]):
    """
    :param message:
    :param animes: json response from shikimori
    :return: None
    """
    kb = await inline.animes_from_shikimori_kb(animes)
    await message.edit_caption(
        "Нажмите на интересующее вас Аниме, \nкоторое было найдено на Shikimori",
        reply_markup=kb,
    )


async def edit_all_follows_markup(message: types.Message, action, page):
    """this method implements pagination with reply_markup"""
    follows = await anilibria_repository.get_all_follows_by_user(message.chat.id)
    kb = await all_follows_kb(follows.follows, action, page)
    await dp.bot.edit_message_reply_markup(
        message.chat.id, message.message_id, reply_markup=kb
    )
