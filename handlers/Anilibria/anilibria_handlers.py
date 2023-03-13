from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot import db_client
from .anime_functions import search_on_anilibria
from .other_functional import display_anime_al
from .states import AnimeFollow


async def anime_follow_start(message: types.Message):
    """Standard start function for state"""
    await message.answer('Напиши название тайтла, а я его поищу')
    await AnimeFollow.anime_title.set()


async def anime_follow_end(message: types.Message, state: FSMContext):
    """get anime_title, and insert into db"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_follow_search']
    # trash collector
    collection.delete_many({'chat_id': message.chat.id})
    # insert new data
    data = await search_on_anilibria(message.text)
    collection.insert_one({'chat_id': message.chat.id,
                           'animes': data['list'],
                           'page': 0})

    await display_anime_al(message, 'anime_follow_search')
    await state.finish()


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_follow_start, commands=['/AnimeFollow'])
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
