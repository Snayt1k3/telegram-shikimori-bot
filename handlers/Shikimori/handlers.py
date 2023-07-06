import os

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from Keyboard.inline import inline_kb_tf
from Keyboard.reply import default_keyboard
from bot import dp
from database.database import DataBase
from misc.constants import get_headers, SHIKI_URL
from .helpful_functions import DisplayUserLists, AnimeMarkDisplay
from .oauth import get_first_token
from .shikimori_requests import ShikimoriRequests
from .states import UserNicknameState, AnimeMarkState
from .validation import check_user_shiki_id, check_user_in_database


async def SetNickname(message: types.Message):
    """
    If user call command /GetProfile first time, we add user id into db
    else call method UserProfile which send user profile
    """
    user_id = await ShikimoriRequests.GetShikiId(message.chat.id)
    if not user_id:  # here check if user already have nick from shiki
        await UserNicknameState.auth_code.set()
        await message.answer(hlink("Жмяк",
                                   f'{SHIKI_URL}oauth/authorize?client_id='
                                   f'{os.environ.get("CLIENT_ID")}'
                                   f'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
                                   f'&response_type=code&scope='),
                             parse_mode='HTML')
        await message.answer("Отправьте мне свой код авторизации.")
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
                                    f"Никнейм: <b>{res['nickname']}</b>\n"
                                    f"id: {res['id']}\n"
                                    f"Запланированное - {anime_stats[0]['size']}\n"
                                    f"Смотрю - {anime_stats[1]['size']}\n"
                                    f"Просмотрено - {anime_stats[2]['size']}\n"
                                    f"Брошено - {anime_stats[4]['size']}\n"
                                    f"{hlink('Мой Профиль', SHIKI_URL + res['nickname'])}",
                                    parse_mode="HTML",
                                    reply_markup=default_keyboard)


async def GetAuthCode(message: types.Message, state: FSMContext):
    if not DataBase.find_one('chat_id', message.chat.id, 'users_id'):  # check exists user in table
        DataBase.insert_into_collection('users_id', {"chat_id": message.chat.id,
                                                     "shikimori_id": None,
                                                     "access_token": None,
                                                     "refresh_token": None,
                                                     "auth_code": None})

    await state.finish()

    # validation auth code
    ans = await get_first_token(message.text)
    if ans is None:
        await message.answer("Вы отправили неверный код авторизации 🙁")
        return

    # update if code is correct
    DataBase.update_one('users_id', 'chat_id', message.chat.id, {'auth_code': message.text,
                                                                 'access_token': ans['access_token'],
                                                                 'refresh_token': ans['refresh_token']})

    await check_user_shiki_id(message.chat.id)  # check user truth
    await message.answer("Вы успешно привязали свой профиль 😀",
                         reply_markup=default_keyboard)


async def ResetProfile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer("Вы уверены, что хотите отвязать свой профиль?", reply_markup=inline_kb_tf)


async def UserWatching(message: types.Message):
    """call pagination with parameters which need for watch_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "watching", 'anime_watching')


async def UserPlanned(message: types.Message):
    """call pagination with parameters which need for planned_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "planned", 'anime_planned')


async def UserCompleted(message: types.Message):
    """call pagination with parameters which need for completed_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "completed", 'anime_completed')


async def AnimeMarkStart(message: types.Message):
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return

    await AnimeMarkState.anime_title.set()
    await message.answer("Напишите названия аниме, которое вы хотите найти. \n"
                         "Можете отменить - /cancel")


async def AnimeMarkEnd(message: types.Message, state: FSMContext):
    await state.finish()
    anime_ls = await ShikimoriRequests.SearchShikimoriTitle(message.text)
    await AnimeMarkDisplay(message, anime_ls)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ResetProfile, lambda msg: "UnLink Profile" in msg.text)
    dp.register_message_handler(SetNickname, lambda msg: "Profile" in msg.text)
    dp.register_message_handler(GetAuthCode, state=UserNicknameState.auth_code)

    dp.register_message_handler(AnimeMarkStart, lambda msg: "Mark" in msg.text)
    dp.register_message_handler(AnimeMarkEnd, state=AnimeMarkState.anime_title)

    dp.register_message_handler(UserWatching, lambda msg: "Watch List" in msg.text)
    dp.register_message_handler(UserPlanned, lambda msg: "Planned List" in msg.text)
    dp.register_message_handler(UserCompleted, lambda msg: "Completed List" in msg.text)
