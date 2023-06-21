import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.reply import default_keyboard
from bot import dp
from database.database import DataBase
from handlers.translator import translate_text
from misc.constants import get_headers, SHIKI_URL, PER_PAGE
from .states import AnimeSearch


async def anime_search_start(message: types.Message):
    """This method a start state AnimeSearch"""
    await AnimeSearch.anime_str.set()
    await message.answer(await translate_text(message, "Write what anime you want to find, you can /cancel"))


async def anime_search(message: types.Message, state: FSMContext):
    """This method make a request, after send 10 anime which found"""
    await state.finish()

    # db
    db = DataBase()
    db.trash_collector('chat_id', message.chat.id, 'anime_search')

    ins_data = []

    async with aiohttp.ClientSession(headers=await get_headers(message.chat.id)) as session:
        async with session.get(f"{SHIKI_URL}api/animes?search={message.text}&limit={PER_PAGE}") as response:
            anime_founds = await response.json()

    kb = InlineKeyboardMarkup()
    lang_code = message.from_user.language_code
    for anime in anime_founds:
        ins_data.append(anime['id'])
        kb.add(InlineKeyboardButton(text=anime['name'] if lang_code == 'en' else anime['russian'],
                                    callback_data=f"anime_search.{anime['id']}.view"))

    # insert data in db
    db.insert_into_collection('anime_search', {"chat_id": message.chat.id,
                                               'animes': ins_data})

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"anime_search.0.cancel"))

    await dp.bot.send_photo(message.chat.id, open('misc/searching.png', 'rb'),
                            reply_markup=kb,
                            caption=await translate_text(message, 'Here are the anime that were found'))


async def cancel_handler(message: types.Message, state: FSMContext):
    """This handler allow cancel any states"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('ОК', reply_markup=default_keyboard)


def register_anime_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    dp.register_message_handler(anime_search_start, lambda msg: "Anime Search" in msg.text)
    dp.register_message_handler(anime_search, state=AnimeSearch.anime_str)

