from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from Keyboard.inline import anilibria_allfollow_kb, anilibria_follow_kb
from bot import db_client, dp
from .anime_functions import search_on_anilibria
from .other_functional import display_anime_al, get_anime_info
from .states import AnimeFollow
from misc.constants import ani_url


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


async def all_follows(message: types.Message):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']

    # check user follow anime exists
    record = collection.find_one({'chat_id': message.chat.id})
    #
    if not record['animes']:
        await message.answer('У вас нету ни одного Аниме в подписках')
        return

    # get datas
    record = await get_anime_info(record['animes'][record['page']])
    record = await get_anime_info(8644)

    # send msg
    await dp.bot.send_photo(chat_id=message.chat.id, photo=ani_url + record['posters']['small']['url'],
                            reply_markup=anilibria_allfollow_kb,
                            caption=f"Название: {record['names']['ru']}\n"
                                    f"Жанры: {', '.join(record['genres'])}\n"
                                    f"Озвучили: {', '.join(record['team']['voice'])}\n"
                                    f"Эпизоды: {record['type']['full_string']}")


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_follow_start, commands=['AnimeFollow'])
    dp.register_message_handler(all_follows, commands=['MyFollow'])
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
