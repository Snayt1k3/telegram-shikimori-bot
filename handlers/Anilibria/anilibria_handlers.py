from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import db_client, dp
from .helpful_functions import get_anime_info, search_on_anilibria, display_search_anime
from .states import AnimeFollow, start_get_torrent


async def anime_follow_start(message: types.Message):
    """Standard start function for state"""
    await message.answer('Напиши название тайтла, а я его поищу')
    await AnimeFollow.anime_title.set()


async def anime_follow_end(message: types.Message, state: FSMContext):
    """get anime_title, and insert into db"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_search_al']
    # trash collector
    collection.delete_many({'chat_id': message.chat.id})
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


async def anime_get_torrent(message: types.Message):
    await start_get_torrent(message)


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_follow_start, lambda msg: 'Follow to Anime' in msg.text)
    dp.register_message_handler(all_follows, lambda msg: 'My Follows' in msg.text)
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
    dp.register_message_handler(anime_get_torrent, lambda msg: 'Get torrent' in msg.text)

