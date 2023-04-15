import os

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from .validation import check_user_shiki_id
from Keyboard.inline import inline_kb_tf
from Keyboard.reply import default_keyboard
from bot import dp, db_client
from handlers.translator import translate_text
from misc.constants import get_headers, shiki_url
from .helpful_functions import get_shiki_id_by_chat_id, start_pagination_user_lists
from .oauth import get_first_token
from .states import UserNickname


async def set_user_nickname(message: types.Message):
    """If user call command /GetProfile first time, we add user id into db
    else call method user_profile Which send user profile"""

    user_id = await get_shiki_id_by_chat_id(message.chat.id)
    # here check if user already have nick from shiki
    if not user_id:
        await UserNickname.auth_code.set()
        await message.answer(await translate_text(message,
                             hlink("Click here",
                                   f'{shiki_url}oauth/authorize?client_id='
                                   f'{os.environ.get("CLIENT_ID")}'
                                   f'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
                                   f'&response_type=code&scope=')),
                             parse_mode='HTML')
        await message.answer(await translate_text(message, "Send me your auth code"))
    else:
        await user_profile(message)


async def user_profile(message: types.Message):
    """This method send a user profile and information from profile"""
    async with aiohttp.ClientSession(headers=await get_headers(message.chat.id)) as session:
        user_id = await get_shiki_id_by_chat_id(message.chat.id)
        async with session.get(f"{shiki_url}api/users/{user_id}") as response:
            res = await response.json()
            anime_stats = res['stats']['statuses']['anime']
            await dp.bot.send_photo(message.chat.id, res['image']['x160'],
                                    await translate_text(message,
                                                         f"Your Profile\n"
                                                         f"Nickname: <b>{res['nickname']}</b>\n"
                                                         f"Your id: {res['id']}\n"
                                                         f"Planned - {anime_stats[0]['size']}\n"
                                                         f"Watching - {anime_stats[1]['size']}\n"
                                                         f"Completed - {anime_stats[2]['size']}\n"
                                                         f"Abandoned - {anime_stats[4]['size']}\n"
                                                         f"{hlink('Go to my Profile', shiki_url + res['nickname'])}"),
                                    parse_mode="HTML")


async def get_user_auth_code(message: types.Message, state: FSMContext):
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection ids_users
    collection = db_current["ids_users"]
    # insert one record
    if not collection.find_one({'chat_id': message.chat.id}):
        collection.insert_one({"chat_id": message.chat.id,
                               "shikimori_id": None,
                               "access_token": None,
                               "refresh_token": None,
                               "auth_code": None})

    ans = await get_first_token(message.text)
    await state.finish()
    if ans is None:
        await message.answer(await translate_text(message, "You send a wrong auth code"))
        return

    # update one record
    collection.update_one({"chat_id": message.chat.id}, {"$set": {'auth_code': message.text,
                                                                  'access_token': ans['access_token'],
                                                                  'refresh_token': ans['refresh_token']}})
    await check_user_shiki_id(message.chat.id)
    await message.answer(await translate_text(message, "Your Profile has been linked"),
                         reply_markup=default_keyboard)


async def reset_user_profile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer(await translate_text(message, "Are You sure?"), reply_markup=inline_kb_tf)


async def get_user_watching(message: types.Message):
    """call pagination with parameters which need for watch_list"""
    await start_pagination_user_lists(message, "watching", 'anime_watching', 'Смотрю')


async def get_user_planned(message: types.Message):
    """call pagination with parameters which need for planned_list"""
    await start_pagination_user_lists(message, "planned", 'anime_planned', 'Запланированного')


async def get_user_completed_list(message: types.Message):
    """call pagination with parameters which need for completed_list"""
    await start_pagination_user_lists(message, "completed", 'anime_completed', 'Просмотрено')


def register_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(set_user_nickname, lambda msg: "My Profile" in msg.text)
    dp.register_message_handler(get_user_auth_code, state=UserNickname.auth_code)

    dp.register_message_handler(reset_user_profile, lambda msg: "Reset Profile" in msg.text)

    dp.register_message_handler(get_user_watching, lambda msg: "My Watch List" in msg.text)

    dp.register_message_handler(get_user_planned, lambda msg: "My Planned List" in msg.text)

    dp.register_message_handler(get_user_completed_list, lambda msg: "My Completed List" in msg.text)
