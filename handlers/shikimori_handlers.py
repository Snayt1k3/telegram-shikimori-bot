import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from telegram_bot_pagination import InlineKeyboardPaginator

from bot import dp, db_client

headers = {
    'User-Agent': 'Snayt1k3',
    'Authorization': 'Bearer ',
}

shiki_url = "https://shikimori.one/"


class AnimeSearch(StatesGroup):
    anime_str = State()


async def anime_search_start(message: types.Message):
    await AnimeSearch.anime_str.set()
    await message.reply("Write what anime you want to find")


async def anime_search(message: types.Message, state: FSMContext):
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]


    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/animes?search={message.text}&limit=5") as response:
            anime_founds = await response.json()
            collection.insert_one({"message_id": message.message_id,
                                   "message_text": anime_founds})

    await anime_search_pagination(message, db_message_id=message.message_id)
    await state.finish()


async def anime_search_pagination(message: types.message, db_message_id, page=1):
    """
    :param message:
    :param db_message_id: This parameter is needed to search the response in the database
    :param page:
    """


    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]
    anime_founds = collection.find_one({"message_id": int(db_message_id)})['message_text']

    # Pagination
    paginator = InlineKeyboardPaginator(
        5,
        current_page=page,
        data_pattern=f'anime_founds.{db_message_id}' + '#{page}'
    )

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=paginator.markup,
                            photo=shiki_url + anime_founds[page - 1]['image']['original'],
                            parse_mode="HTML",
                            caption=f"Eng: <b> {anime_founds[page - 1]['name']} </b> \n"
                                    f"Rus: <b> {anime_founds[page - 1]['russian']} </b> \n"
                                    f"Rating: <b> {anime_founds[page - 1]['score']}</b> \n"
                                    f"Episode Count: <b> {anime_founds[page - 1]['episodes']} </b> \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_founds[page - 1]['url'])}"
                            )


async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    await dp.bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await anime_search_pagination(message=call.message, page=page, db_message_id=call.data.split('#')[0].split('.')[1])


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_search_start, commands=['AnimeSearch'])
    dp.register_message_handler(anime_search, state=AnimeSearch.anime_str)
    dp.register_callback_query_handler(characters_page_callback, lambda call: call.data.split('.')[0] == 'anime_founds')
