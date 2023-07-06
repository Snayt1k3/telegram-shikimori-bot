import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.database import DataBase
from bot import dp
from .helpful_functions import get_anime_info_from_al, search_on_anilibria, display_search_anime
from .states import AnimeFollow, start_get_torrent


async def anime_follow_start(message: types.Message):
    """Standard start function for state"""
    await message.answer('Напиши название тайтла, а я его поищу.\n'
                         'Можете отменить - /cancel')
    await AnimeFollow.anime_title.set()


async def anime_follow_end(message: types.Message, state: FSMContext):
    """get anime_title, and insert into db"""
    db = DataBase()
    db.trash_collector('chat_id', message.chat.id, 'anime_search_al')
    data = await search_on_anilibria(message.text)

    # validation data
    if not data:
        await message.answer('Ничего не найдено.')
        return

    db.insert_into_collection('anime_search_al', {'chat_id': message.chat.id,
                                                  'animes': [anime['id'] for anime in data['list']]})

    await display_search_anime(message)
    await state.finish()


async def all_follows(message: types.Message):
    """send all follows list to user"""
    db = DataBase()
    record = db.find_one('chat_id', message.chat.id, 'user_follows')

    if not record or not record['animes']:
        await message.answer('У вас нету ни одного аниме в подписках')
        return

    kb = InlineKeyboardMarkup()

    # get all responses
    tasks = [get_anime_info_from_al(anime_id) for anime_id in record['animes'][:8]]
    responses = await asyncio.gather(*tasks)

    for anime_info in responses:
        kb.add(InlineKeyboardButton(anime_info['names']['ru'], callback_data=f'view.{anime_info["id"]}.all_follows'))

    if len(record['animes']) > 8:
        kb.add(InlineKeyboardButton('>>', callback_data='next.0.all_follows'))

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'), "Нажмите на интересующее вас аниме",
                            reply_markup=kb)


async def anime_get_torrent(message: types.Message):
    await start_get_torrent(message)


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_follow_start, lambda msg: 'Follow to Anime' in msg.text)
    dp.register_message_handler(all_follows, lambda msg: 'Follows' in msg.text)
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
    dp.register_message_handler(anime_get_torrent, lambda msg: 'torrent' in msg.text)

