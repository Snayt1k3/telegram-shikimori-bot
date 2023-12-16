from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.inline import AnimeMarkEdit_Kb
from bot import dp
from database.animedb import AnimeDB
from database.database import db_repository
from misc.constants import SHIKI_URL, PER_PAGE
from utils.message import message_work
from .shiki_api import ShikimoriApiClient


async def edit_message_for_view_anime(
    message: types.Message, kb, anime_info, user_rate
):
    """
    Editing msg, for manage anime
    :param message: Telegram Message
    :param kb: Inline Keyboard
    :param anime_info: info about anime
    :param user_rate: Info about user rate
    """
    await message.bot.edit_message_media(
        types.InputMediaPhoto(SHIKI_URL + anime_info["image"]["original"]),
        message.chat.id,
        message.message_id,
    )

    await message.bot.edit_message_caption(
        message.chat.id,
        message.message_id,
        reply_markup=kb,
        caption=await message_work.anime_info_rate_msg(user_rate, anime_info),
    )


async def PaginationMarkupLists(message: types.Message, coll, action, page):
    """
    This func implements pagination for planned, watching, completed lists, by inline Keyboard
    :param message: Telegram Message
    :param coll: name of Mongo collection
    :param action: plus or minus
    :param page: number of page
    """

    # action with page
    if action == "-":
        page -= int(PER_PAGE)
    else:
        page += int(PER_PAGE)

    animes = await AnimeDB.get_shiki_list(message.chat.id, coll, page)
    kb = InlineKeyboardMarkup()

    # check requests responses
    if not all(animes):
        await message.answer("Что-то пошло не так, попробуйте еще раз.")
        return

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru, callback_data=f"{coll}.{anime.id}.{page}.view.user_list"
            )
        )

    # Kb actions
    if len(animes) == 8 and page != 0:
        kb.add(
            InlineKeyboardButton("<<", callback_data=f"{coll}.0.{page}.prev.user_list"),
            InlineKeyboardButton(">>", callback_data=f"{coll}.0.{page}.next.user_list"),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton("<<", callback_data=f"{coll}.0.{page}.prev.user_list")
        )
    else:
        kb.add(
            InlineKeyboardButton(">>", callback_data=f"{coll}.0.{page}.next.user_list"),
        )

    await message.bot.edit_message_reply_markup(
        message.chat.id, message.message_id, reply_markup=kb
    )


async def DisplayUserLists(message: types.Message, status, coll, is_edit=False, page=0):
    """
    Sends a message with the list specified in the arguments
    :param message: Telegram Message
    :param status: one of lists from shikimori
    :param coll: name of collection from Mongo
    :param is_edit: flag is required to when user use back button
    :param page: number of page
    """

    if not is_edit:
        animes = await ShikimoriApiClient.get_animes_by_status(message.chat.id, status)
        animes = await AnimeDB.insert_shiki_list(
            message.chat.id, coll, [anime["target_id"] for anime in animes]
        )
        animes = animes[page : page + 8]
    else:
        animes = await AnimeDB.get_shiki_list(message.chat.id, coll, page)

    # Keyboard object
    kb = InlineKeyboardMarkup()
    page = int(page)

    # check requests responses
    if not all(animes):
        await message.answer("Что-то пошло не так, попробуйте еще раз.")
        return

    for anime in animes:
        # add buttons
        kb.add(
            InlineKeyboardButton(
                text=anime.title_ru, callback_data=f"{coll}.{anime.id}.0.view.user_list"
            )
        )
    # check page for pagination
    if len(animes) == 8 and page > 0:
        kb.add(
            InlineKeyboardButton("<<", callback_data=f"{coll}.0.{page}.prev.user_list"),
            InlineKeyboardButton(">>", callback_data=f"{coll}.0.{page}.next.user_list"),
        )

    elif page > 0:  # if we not on a first page
        kb.add(
            InlineKeyboardButton("<<", callback_data=f"{coll}.0.{page}.prev.user_list")
        )
    else:  # if we on a first page
        kb.add(
            InlineKeyboardButton(">>", callback_data=f"{coll}.0.{page}.next.user_list"),
        )

    if not is_edit:
        await message.bot.send_photo(
            message.chat.id,
            open("misc/img/pic1.png", "rb"),
            reply_markup=kb,
            caption="Выберите интересующее вас аниме.",
        )
    else:
        await message.bot.edit_message_media(
            types.InputMediaPhoto(open("misc/img/pic1.png", "rb")),
            message.chat.id,
            message.message_id,
        )

        await dp.bot.edit_message_caption(
            message.chat.id,
            message.message_id,
            caption="Выберите интересующее вас аниме.",
            reply_markup=kb,
        )


async def AnimeMarkDisplay(msg: types.Message, anime_ls=None, is_edit=False):
    """
    Send msg with inline buttons with anime which found, or edit msg for 'back'
    :param msg: Telegram Message
    :param anime_ls: uses when user already call mark command
    :param is_edit: flag is required to when user use back button
    """
    if anime_ls:
        await db_repository.delete_many(
            filter={"chat_id": msg.chat.id}, collection="Anime_Mark"
        )
        anime_ls = await AnimeDB.insert_shiki_list(
            msg.chat.id, "Anime_Mark", [anime["id"] for anime in anime_ls]
        )

    if anime_ls is None:  # if we call method from callback or use back btn
        anime_ls = await AnimeDB.get_shiki_list(msg.chat.id, "Anime_Mark", 0)

    kb = InlineKeyboardMarkup()

    for anime in anime_ls:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru, callback_data=f"view.{anime.id}.anime_mark"
            )
        )

    kb.add(InlineKeyboardButton("❌ Отмена", callback_data=f"cancel.0.anime_mark"))

    if is_edit:
        await msg.edit_media(
            media=types.InputMediaPhoto(open("misc/img/pic1.png", "rb"))
        )
        await msg.edit_caption(
            reply_markup=kb, caption="Выберите интересующее вас аниме."
        )

    else:
        await msg.bot.send_photo(
            msg.chat.id,
            open("misc/img/pic1.png", "rb"),
            "Выберите интересующее вас аниме.",
            reply_markup=kb,
        )


async def AnimeMarkDisplayEdit(msg: types.Message, anime_id):
    """
    edit msg for manage anime
    :param msg: Telegram Message
    :param anime_id: id from shikimori
    """
    # get info about anime
    anime = await ShikimoriApiClient.get_anime(anime_id)

    # create kb with anime_id
    kb = AnimeMarkEdit_Kb(anime_id)

    await msg.edit_media(types.InputMediaPhoto(SHIKI_URL + anime["image"]["original"]))

    await msg.edit_caption(
        await message_work.anime_info_msg(anime),
        reply_markup=kb,
    )
