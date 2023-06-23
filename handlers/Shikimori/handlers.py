import os

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink
from .shikimori_requests import ShikimoriRequests
from Keyboard.inline import inline_kb_tf
from Keyboard.reply import default_keyboard
from bot import dp
from database.database import DataBase
from handlers.translator import translate_text
from misc.constants import get_headers, SHIKI_URL, PER_PAGE
from .helpful_functions import start_pagination_user_lists, AnimeMarkDisplay
from .oauth import get_first_token
from .states import AnimeSearchState, UserNicknameState, AnimeMarkState
from .validation import check_user_shiki_id


async def AnimeSearchStart(message: types.Message):
    """This method a start state AnimeSearchState"""
    await AnimeSearchState.anime_str.set()
    await message.answer(await translate_text(message, "Write what anime you want to find, you can /cancel"))


async def AnimeSearch(message: types.Message, state: FSMContext):
    """This method make a request, after send 10 anime which found"""
    await state.finish()

    db = DataBase()
    db.trash_collector('chat_id', message.chat.id, 'anime_search')

    data = []

    async with aiohttp.ClientSession(headers=await get_headers(message.chat.id)) as session:
        async with session.get(f"{SHIKI_URL}api/animes?search={message.text}&limit={PER_PAGE}") as response:
            anime_founds = await response.json()

    kb = InlineKeyboardMarkup()
    lang_code = message.from_user.language_code
    for anime in anime_founds:
        data.append(anime['id'])
        kb.add(InlineKeyboardButton(text=anime['russian'] if lang_code == 'ru' else anime['name'],
                                    callback_data=f"view.{anime['id']}.anime_search"))

    # insert data in db
    db.insert_into_collection('anime_search', {"chat_id": message.chat.id,
                                               'animes': data})

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"anime_search.0.cancel"))

    await dp.bot.send_photo(message.chat.id, open('misc/searching.png', 'rb'),
                            reply_markup=kb,
                            caption=await translate_text(message, 'Here are the anime that were found'))


async def SetNickname(message: types.Message):
    """
    If user call command /GetProfile first time, we add user id into db
    else call method UserProfile which send user profile
    """
    user_id = await ShikimoriRequests.GetShikiId(message.chat.id)
    if not user_id:  # here check if user already have nick from shiki
        await UserNicknameState.auth_code.set()
        await message.answer(await translate_text(message,
                                                  hlink("Click here",
                                                        f'{SHIKI_URL}oauth/authorize?client_id='
                                                        f'{os.environ.get("CLIENT_ID")}'
                                                        f'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
                                                        f'&response_type=code&scope=')),
                             parse_mode='HTML')
        await message.answer(await translate_text(message, "Send me your auth code"))
    else:
        await UserProfile(message)


async def UserProfile(message: types.Message):
    """This method send a user profile and information from profile"""
    user_id = await ShikimoriRequests.GetShikiId(message.chat.id)

    async with aiohttp.ClientSession(headers=await get_headers(message.chat.id)) as session:
        async with session.get(f"{SHIKI_URL}api/users/{user_id}") as response:
            res = await response.json()
            anime_stats = res['stats']['statuses']['anime']
            await dp.bot.send_photo(message.chat.id, res['image']['x160'],
                                    await translate_text(message,
                                                         f"Nickname: <b>{res['nickname']}</b>\n"
                                                         f"Your id: {res['id']}\n"
                                                         f"Planned - {anime_stats[0]['size']}\n"
                                                         f"Watching - {anime_stats[1]['size']}\n"
                                                         f"Completed - {anime_stats[2]['size']}\n"
                                                         f"Abandoned - {anime_stats[4]['size']}\n"
                                                         f"{hlink('Go to my Profile', SHIKI_URL + res['nickname'])}"),
                                    parse_mode="HTML",
                                    reply_markup=default_keyboard)


async def GetAuthCode(message: types.Message, state: FSMContext):
    db = DataBase()
    if not db.find_one('chat_id', message.chat.id, 'ids_users'):  # check exists user in table
        db.insert_into_collection('ids_users', {"chat_id": message.chat.id,
                                                "shikimori_id": None,
                                                "access_token": None,
                                                "refresh_token": None,
                                                "auth_code": None})

    await state.finish()

    # validation auth code
    ans = await get_first_token(message.text)
    if ans is None:
        await message.answer(await translate_text(message, "You send a wrong auth code"))
        return

    # update if code is correct
    db.update_one('ids_users', 'chat_id', message.chat.id, {'auth_code': message.text,
                                                            'access_token': ans['access_token'],
                                                            'refresh_token': ans['refresh_token']})

    await check_user_shiki_id(message.chat.id)  # check user truth
    await message.answer(await translate_text(message, "Your Profile has been linked"),
                         reply_markup=default_keyboard)


async def ResetProfile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer(await translate_text(message, "Are You sure?"), reply_markup=inline_kb_tf)


async def UserWatching(message: types.Message):
    """call pagination with parameters which need for watch_list"""
    await start_pagination_user_lists(message, "watching", 'anime_watching')


async def UserPlanned(message: types.Message):
    """call pagination with parameters which need for planned_list"""
    await start_pagination_user_lists(message, "planned", 'anime_planned')


async def UserCompleted(message: types.Message):
    """call pagination with parameters which need for completed_list"""
    await start_pagination_user_lists(message, "completed", 'anime_completed')


async def AnimeMarkStart(message: types.Message):
    await AnimeMarkState.anime_title.set()
    await message.answer(await translate_text(message, "Write an anime that you want to find"))


async def AnimeMarkEnd(message: types.Message, state: FSMContext):
    await state.finish()
    anime_ls = await ShikimoriRequests.SearchShikimoriTitle(message.text)
    await AnimeMarkDisplay(message, anime_ls)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(AnimeSearchStart, lambda msg: "Search" in msg.text)
    dp.register_message_handler(AnimeSearch, state=AnimeSearchState.anime_str)

    dp.register_message_handler(ResetProfile, lambda msg: "UnLink Profile" in msg.text)
    dp.register_message_handler(SetNickname, lambda msg: "Profile" in msg.text)
    dp.register_message_handler(GetAuthCode, state=UserNicknameState.auth_code)

    dp.register_message_handler(AnimeMarkStart, lambda msg: "Mark" in msg.text)
    dp.register_message_handler(AnimeMarkEnd, state=AnimeMarkState.anime_title)

    dp.register_message_handler(UserWatching, lambda msg: "Watch List" in msg.text)
    dp.register_message_handler(UserPlanned, lambda msg: "Planned List" in msg.text)
    dp.register_message_handler(UserCompleted, lambda msg: "Completed List" in msg.text)
