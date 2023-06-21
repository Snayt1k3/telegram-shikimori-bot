import asyncio

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hlink
from database.database import DataBase
from Keyboard.inline import cr_kb_search_edit
from bot import dp
from handlers.translator import translate_text
from misc.constants import SHIKI_URL, PER_PAGE
from .shikimori_requests import ShikimoriRequests


async def edit_message_for_view_anime(message: types.Message, kb, anime_info, user_rate):
    await dp.bot.edit_message_media(types.InputMediaPhoto(SHIKI_URL + anime_info['image']['original']), message.chat.id,
                                    message.message_id)

    await dp.bot.edit_message_caption(message.chat.id, message.message_id,
                                      reply_markup=kb,
                                      parse_mode='HTML',
                                      caption=f"<b>Eng</b>: {anime_info['name']}  \n"
                                              f"<b>Rus</b>: {anime_info['russian']} \n"
                                              f"<b>Rating</b>: {anime_info['score']}\n"
                                              f"<b>Your Rating</b>: {user_rate['score']}\n"
                                              f"<b>Viewed</b>: {user_rate['episodes']} "
                                              f": {anime_info['episodes']} \n" +
                                              hlink(await translate_text(message, 'Go to the Anime'),
                                                    SHIKI_URL + anime_info['url'])
                                      )


async def edit_reply_markup_user_lists(message: types.Message, coll, action, page):
    """This func implements pagination for planned, watching, completed lists, by Keyboard,
    this method edit Keyboard(Inline) for Each page"""

    # DataBase
    db = DataBase()
    record = db.find_one('chat_id', message.chat.id, coll)

    # action with page
    if action == '-':
        page -= int(PER_PAGE)
    else:
        page += int(PER_PAGE)

    kb = InlineKeyboardMarkup()

    tasks = [ShikimoriRequests.GetAnimeSemaphore(anime)
             for anime in record['animes'][page: page + int(PER_PAGE)]]
    anime_info = await asyncio.gather(*tasks)

    for anime in anime_info:
        kb.add(InlineKeyboardButton(anime['russian'],
                                    callback_data=f"{coll}.{anime['id']}.{page}.view.user_list"))

    # Kb actions
    if len(record['animes']) > page + int(PER_PAGE) and page != 0:
        kb.add(
            InlineKeyboardButton(text='<<', callback_data=f'{coll}.0.{page}.prev.user_list'),
            InlineKeyboardButton(text='>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton(text='<<', callback_data=f'{coll}.0.{page}.prev.user_list'))
    else:
        kb.add(
            InlineKeyboardButton(text='>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    await dp.bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=kb)


async def start_pagination_user_lists(message: types.Message, status, coll):
    """Implements display for all user lists"""
    animes = await ShikimoriRequests.GetAnimesByStatusId(message.chat.id, status)

    # DataBase
    db = DataBase()
    db.trash_collector('chat_id', message.chat.id, coll)
    db.insert_into_collection(coll, {'chat_id': message.chat.id,
                                     "animes": [anime['target_id'] for anime in animes]})

    # Keyboard object
    kb = InlineKeyboardMarkup()

    # semaphore (shikimori have 5rps only)
    tasks = [ShikimoriRequests.GetAnimeSemaphore(anime['target_id'])
             for anime in animes[:int(PER_PAGE)]]
    animes_info = await asyncio.gather(*tasks)

    for anime in animes_info:
        # add pretty buttons for action with user list
        kb.add(InlineKeyboardButton(text=anime['russian'],
                                    callback_data=f"{coll}.{anime['id']}.0.view.user_list"))
    # check list for pagination
    if len(animes) > int(PER_PAGE):
        kb.add(InlineKeyboardButton('>>',
                                    callback_data=f"{coll}.0.0.next.user_list"))

    await dp.bot.send_photo(message.chat.id, open('misc/list.png', 'rb'),
                            reply_markup=kb,
                            caption=await translate_text(message, 'Выберите Интересующее вас аниме'))


async def anime_search_edit(message: types.Message, target_id):
    anime_info = await ShikimoriRequests.GetAnimeInfo(target_id)
    await dp.bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id,
                                    media=types.InputMediaPhoto(SHIKI_URL + anime_info['image']['original']))

    kb = cr_kb_search_edit(target_id)
    await dp.bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                      parse_mode='HTML',
                                      reply_markup=kb,
                                      caption=f"<b>{anime_info['name']}</b> — <b>{anime_info['russian']}</b>\n\n"
                                              f"<b>Genres</b>: "
                                              f"{', '.join([genre['name'] for genre in anime_info['genres']])}\n"
                                              f"<b>Status</b>: {anime_info['status']} \n"
                                              f"<b>Rating</b>: {anime_info['score']} \n"
                                              f"<b>Ep</b>: {anime_info['episodes']} \n" +
                                              hlink(await translate_text(message, 'Go to the Anime'),
                                                    SHIKI_URL + anime_info['url']))


async def display_user_list(message: types.Message, coll, page):
    """Call when user click on back button"""

    # Db
    db = DataBase()
    record = db.find_one('chat_id', message.chat.id, coll)

    kb = InlineKeyboardMarkup()
    page = int(page)

    # semaphore (shikimori have 5rps only)
    tasks = [ShikimoriRequests.GetAnimeSemaphore(anime)
             for anime in record['animes'][page: page + int(PER_PAGE)]]
    animes_info = await asyncio.gather(*tasks)

    for anime_info in animes_info:
        kb.add(InlineKeyboardButton(anime_info['russian'],
                                    callback_data=f"{coll}.{anime_info['id']}.{page}.view.user_list"))

    # Kb actions
    if len(record['animes']) > page + int(PER_PAGE) and page != 0:
        kb.add(
            InlineKeyboardButton(text='<<', callback_data=f'{coll}.0.{page}.prev.user_list'),
            InlineKeyboardButton(text='>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton(text='<<', callback_data=f'{coll}.0.{page}.prev.user_list'))
    else:
        kb.add(
            InlineKeyboardButton(text='>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    await dp.bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id,
                                    media=types.InputMediaPhoto(open('misc/list.png', 'rb')))

    await dp.bot.edit_message_caption(message.chat.id, message.message_id,
                                      reply_markup=kb,
                                      caption=await translate_text(message, 'Выберите Интересующее вас аниме'))


async def anime_search_edit_back(message: types.Message):
    """This method implements btn back in anime searching"""

    # get db
    db = DataBase()
    record = db.find_one('chat_id', message.chat.id, 'anime_search')

    kb = InlineKeyboardMarkup()

    # get lang code for pretty display
    lang_code = message.from_user.language_code

    # semaphore
    tasks = [ShikimoriRequests.GetAnimeSemaphore(anime['target_id'])
             for anime in record['animes'][:int(PER_PAGE)]]
    animes_info = await asyncio.gather(*tasks)

    for anime in animes_info:
        kb.add(InlineKeyboardButton(text=anime['name'] if lang_code == 'en' else anime['russian'],
                                    callback_data=f"anime_search.{anime['id']}.view"))

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"anime_search.0.cancel"))

    await dp.bot.edit_message_media(message_id=message.message_id, chat_id=message.chat.id,
                                    media=types.InputMediaPhoto(open("misc/searching.png", 'rb')))

    await dp.bot.edit_message_caption(message_id=message.message_id,
                                      chat_id=message.chat.id,
                                      reply_markup=kb,
                                      caption=await translate_text(message, 'Here are the anime that were found'))
