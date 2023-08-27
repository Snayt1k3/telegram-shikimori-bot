import os

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from Keyboard.inline import inline_kb_tf, keyboard_profile
from Keyboard.reply import default_keyboard
from bot import dp
from database.database import DataBase
from database.animedb import AnimeDB
from misc.constants import get_headers, SHIKI_URL
from .helpful_functions import DisplayUserLists, AnimeMarkDisplay
from .oauth import get_first_token
from .shikimori_requests import ShikimoriRequests
from .states import UserNicknameState, AnimeMarkState
from .validation import check_user_shiki_id, check_user_in_database
from utils.message import message_work


async def SetNickname(message: types.Message):
    """
    If user call command /Profile first time, we add user id into db
    else call method UserProfile which send user profile
    """
    user_id = await ShikimoriRequests.GetShikiId(message.chat.id)
    if not user_id:  # here check if user already have nick from shiki
        await UserNicknameState.auth_code.set()
        await message.answer(
            "Отправьте мне свой код авторизации.\n"
            + hlink(
                "Клик",
                f"{SHIKI_URL}oauth/authorize?client_id="
                f'{os.environ.get("CLIENT_ID")}'
                f"&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
                f"&response_type=code&scope=",
            ),
        )
    else:
        await UserProfile(message)


async def UserProfile(message: types.Message):
    """This method send a user profile and information from profile"""
    user_id = await ShikimoriRequests.GetShikiId(message.chat.id)

    async with aiohttp.ClientSession(
        headers=await get_headers(message.chat.id)
    ) as session:
        async with session.get(f"{SHIKI_URL}api/users/{user_id}") as response:
            kb = await keyboard_profile()
            res = await response.json()
            await dp.bot.send_photo(
                message.chat.id,
                res["image"]["x160"],
                await message_work.profile_msg(res),
                reply_markup=kb,
            )


async def GetAuthCode(message: types.Message, state: FSMContext):
    if not await DataBase.find_one(
        "chat_id", message.chat.id, "users_id"
    ):  # check exists user in table
        await DataBase.insert_into_collection(
            "users_id",
            {
                "chat_id": message.chat.id,
                "shikimori_id": None,
                "access_token": None,
                "refresh_token": None,
                "auth_code": None,
            },
        )

    await state.finish()

    # validation auth code
    ans = await get_first_token(message.text)
    if ans is None:
        await message.answer("Вы отправили неверный код авторизации 🙁")
        return

    # update if code is correct
    await DataBase.update_one(
        "users_id",
        "chat_id",
        message.chat.id,
        {
            "auth_code": message.text,
            "access_token": ans["access_token"],
            "refresh_token": ans["refresh_token"],
        },
    )

    await check_user_shiki_id(message.chat.id)  # check user truth
    await message.answer(
        "Вы успешно привязали свой профиль 😀", reply_markup=default_keyboard
    )


async def ResetProfile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer(
        "Вы уверены, что хотите отвязать свой профиль?", reply_markup=inline_kb_tf
    )


async def UserWatching(message: types.Message):
    """call pagination with parameters which need for watch_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "watching", "anime_watching")


async def UserPlanned(message: types.Message):
    """call pagination with parameters which need for planned_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "planned", "anime_planned")


async def UserCompleted(message: types.Message):
    """call pagination with parameters which need for completed_list"""
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return
    await DisplayUserLists(message, "completed", "anime_completed")


async def AnimeMarkStart(message: types.Message):
    user = await check_user_in_database(message.chat.id)
    if not user:
        await message.answer(
            "Вам нужно привязать свой аккаунт Shikimori, чтобы продолжить."
        )
        return

    await AnimeMarkState.anime_title.set()
    await message.answer(
        "Напишите названия аниме, которое вы хотите найти. \n"
        "Можете отменить - /cancel"
    )


async def AnimeMarkEnd(message: types.Message, state: FSMContext):
    await state.finish()
    anime_ls = await ShikimoriRequests.SearchShikimoriTitle(message.text)
    await AnimeMarkDisplay(message, anime_ls)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(SetNickname, commands=["profile", "Profile"])
    dp.register_message_handler(GetAuthCode, state=UserNicknameState.auth_code)

    dp.register_message_handler(AnimeMarkStart, lambda msg: "Mark" in msg.text)
    dp.register_message_handler(AnimeMarkEnd, state=AnimeMarkState.anime_title)

    dp.register_message_handler(UserWatching, lambda msg: "Watch List" in msg.text)
    dp.register_message_handler(UserPlanned, lambda msg: "Planned List" in msg.text)
    dp.register_message_handler(UserCompleted, lambda msg: "Completed List" in msg.text)
