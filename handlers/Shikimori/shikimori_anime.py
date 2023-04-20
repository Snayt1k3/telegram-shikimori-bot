import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hlink

from Keyboard.reply import default_keyboard, keyboard_status
from bot import dp
from database.database import DataBase
from handlers.translator import translate_text
from misc.constants import get_headers, SHIKI_URL, PER_PAGE
from .shikimori_requests import ShikimoriRequests
from .states import MarkAnime, AnimeSearch
from .validation import check_anime_title, check_user_in_database


async def anime_search_start(message: types.Message):
    """This method a start state AnimeSearch"""
    await AnimeSearch.anime_str.set()
    await message.answer(await translate_text(message, "Write what anime you want to find"))


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


async def mark_anime_start(message: types.Message):
    """Start State and asking anime title"""
    # Checking if the user has linked a profile
    if not await check_user_in_database(message.chat.id):
        return

    # Token check
    await MarkAnime.anime_title.set()
    await message.answer(f"{await translate_text(message, 'Hi, enter the exact name of the anime')} \n\n"
                         f"{await translate_text(message, 'you can cancel')} - /cancel")


async def mark_anime_title(message: types.Message, state: FSMContext):
    """Get title and Asking Rating"""
    anime = await check_anime_title(message.text, message.chat.id)
    async with state.proxy() as data:
        # Validation
        if not anime:
            await state.finish()
            await message.answer(await translate_text(message, 'Anime not found'))

        # Here we send the anime we found
        else:
            await dp.bot.send_photo(chat_id=message.chat.id,
                                    photo=SHIKI_URL + anime['image']['original'],
                                    parse_mode="HTML",
                                    caption=f"Eng: <b> {anime['name']} </b> \n"
                                            f"Rus: <b> {anime['russian']} </b> \n"
                                            f"Rating: <b> {anime['score']}</b> \n"
                                            f"Episode Count': <b> {anime['episodes']} </b> \n" +
                                            hlink(await translate_text(message, 'Go to the Anime'),
                                                  SHIKI_URL + anime['url'])
                                    )
            data['anime'] = anime
            await MarkAnime.next()
            await message.answer(await translate_text(message, "Write an Anime Rating 0 - 10"))


async def mark_anime_score(message: types.Message, state: FSMContext):
    """Get Score and Asking Status"""
    async with state.proxy() as data:
        if not message.text.isdigit() or int(message.text) not in [i for i in range(11)]:
            await message.answer(await translate_text(message, 'Wrong Rating'))
            await state.finish()
        else:
            data['score'] = message.text
            await MarkAnime.next()
            await message.answer(await translate_text(message, "Choose one status"), reply_markup=keyboard_status)


async def mark_anime_status(message: types.Message, state: FSMContext):
    """Get status and finish State"""
    async with state.proxy() as data:
        id_user = await ShikimoriRequests.get_shiki_id(message.chat.id)

        if message.text in ['completed', 'watching', 'planned', 'rewatching', 'dropped']:
            data['status'] = message.text
            await ShikimoriRequests.post_anime_rates(data, id_user, message.chat.id)
            await message.answer(await translate_text(message, "Successfully Recorded"), reply_markup=default_keyboard)
        else:
            await message.answer(await translate_text(message, "Status is not correct"), reply_markup=default_keyboard)

    await state.finish()


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

    dp.register_message_handler(mark_anime_start, lambda msg: "Anime Mark" in msg.text)
    dp.register_message_handler(mark_anime_title, state=MarkAnime.anime_title)
    dp.register_message_handler(mark_anime_status, state=MarkAnime.status)
    dp.register_message_handler(mark_anime_score, state=MarkAnime.score)
