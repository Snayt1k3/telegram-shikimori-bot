from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import db_client, dp
from .anime_functions import search_on_anilibria
from .other_functional import get_anime_info
from .states import AnimeFollow


async def anime_follow_start(message: types.Message):
    """Standard start function for state"""
    await message.answer('Напиши название тайтла, а я его поищу')

    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_follow_search']
    # trash collector
    collection.delete_many({'chat_id': message.chat.id})

    await AnimeFollow.anime_title.set()


async def anime_follow_end(message: types.Message, state: FSMContext):
    """get anime_title, and insert into db"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_search_al']
    # insert new data
    data = await search_on_anilibria(message.text)

    # validation data
    if not data:
        await message.answer('Ничего не найдено')
        return

    collection.insert_one({'chat_id': message.chat.id,
                           'animes': [anime['id'] for anime in data['list']]})

    await display_search_anime(message)
    await state.finish()


async def display_search_anime(message: types.Message):
    # db actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_search_al']
    record = collection.find_one({'chat_id': message.chat.id})

    kb = InlineKeyboardMarkup()

    for anime_id in record['animes'][:10]:
        anime_info = await get_anime_info(anime_id)
        kb.add(InlineKeyboardButton(anime_info['names']['en'], callback_data=f"{anime_id}.search_al"))

    kb.add(InlineKeyboardButton("Cancel", callback_data=f'cancel.search_al'))

    if len(record['animes']) > 10:
        await message.answer("Не все аниме влезли в список, попробуйте написать по точнее")

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'), "Нажмите на Интересующее вас Аниме",
                            reply_markup=kb)


async def all_follows(message: types.Message):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']
    # check user follow anime exists
    record = collection.find_one({'chat_id': message.chat.id})

    if not record or not record['animes']:
        await message.answer('У вас нету ни одного Аниме в подписках')
        return

    kb = InlineKeyboardMarkup()

    for anime_id in record['animes']:
        anime_info = await get_anime_info(anime_id)
        kb.add(InlineKeyboardButton(anime_info['names']['en'], callback_data=f'{anime_id}.all_follows'))

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'), "Нажмите на Интересующее вас Аниме",
                            reply_markup=kb)


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_follow_start, lambda msg: 'Follow to Anime' in msg.text)
    dp.register_message_handler(all_follows, lambda msg: 'My Follows' in msg.text)
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
