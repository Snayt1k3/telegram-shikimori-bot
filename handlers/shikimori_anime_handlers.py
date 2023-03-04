import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from telegram_bot_pagination import InlineKeyboardPaginator

from Keyboard.keyboard import keyboard_status, keyboard_cancel, default_keyboard
from bot import dp, db_client
from constants import headers, shiki_url
from .oauth import check_token
from .validation import check_anime_title


class MarkAnime(StatesGroup):
    anime_title = State()
    score = State()
    status = State()


# Anime Search Start

class AnimeSearch(StatesGroup):
    anime_str = State()


async def anime_search_start(message: types.Message):
    """This method a start state AnimeSearch"""
    # Token check
    await check_token()

    await AnimeSearch.anime_str.set()
    await message.reply("Write what anime you want to find")


async def anime_search(message: types.Message, state: FSMContext):
    """This method make a request, after send 5 anime which found"""
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
    """this callback implements pagination for function anime_search_pagination"""
    page = int(call.data.split('#')[1])
    await dp.bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await anime_search_pagination(message=call.message, page=page, db_message_id=call.data.split('#')[0].split('.')[1])


# Anime Search End

# Anime Mark Start

async def mark_anime_start(message: types.message):
    """Start State and asking anime title"""
    # Token check
    await check_token()
    await MarkAnime.anime_title.set()
    await message.answer("Hi, enter the exact name of the anime", reply_markup=keyboard_cancel)


async def mark_anime_title(message: types.message, state: FSMContext):
    """Get title and Asking Rating"""
    anime = await check_anime_title(message.text)
    async with state.proxy() as data:
        # Validation
        if not anime:
            await state.finish()
            await message.answer('Anime not found')

        # Here we send the anime we found
        else:
            await dp.bot.send_photo(chat_id=message.chat.id,
                                    photo=shiki_url + anime['image']['original'],
                                    parse_mode="HTML",
                                    caption=f"Eng: <b> {anime['name']} </b> \n"
                                            f"Rus: <b> {anime['russian']} </b> \n"
                                            f"Rating: <b> {anime['score']}</b> \n"
                                            f"Episode Count: <b> {anime['episodes']} </b> \n"
                                            f"{hlink('Go to the Anime', shiki_url + anime['url'])}"
                                    )
            data['anime'] = anime
            await MarkAnime.next()
            await message.answer("Write an Anime Rating 0 - 10")


async def mark_anime_score(message: types.message, state: FSMContext):
    """Get Score and Asking Status"""
    async with state.proxy() as data:
        if not message.text.isdigit() or int(message.text) not in [i for i in range(11)]:
            await message.answer('Wrong Rating')
            await state.finish()
        else:
            data['score'] = message.text
            await MarkAnime.next()
            await message.answer("Choose one status", reply_markup=keyboard_status)


async def mark_anime_status(message: types.message, state: FSMContext):
    """Get status and finish State"""
    async with state.proxy() as data:
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        id_user = collection.find_one({"chat_id": message.chat.id})['shikimori_id']
        if message.text in ['completed', 'watching', 'planned', 'rewatching', 'dropped']:
            data['status'] = message.text
            await post_anime_rates(data, id_user)
            await message.answer("Successfully Recorded", reply_markup=default_keyboard)
        else:
            await message.answer("Status is not correct", reply_markup=default_keyboard)

    await state.finish()


async def post_anime_rates(anime_data, id_user):
    """This method make a request(POST), for add new anime on shikimori user profile"""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
                "https://shikimori.one/api/v2/user_rates", json={
                    "user_rate": {
                        "score": anime_data['score'],
                        "status": anime_data['status'],
                        "target_id": anime_data['anime']['id'],
                        "target_type": "Anime",
                        "user_id": id_user,
                    }
                }):
            pass


# Anime Mark End


# Some Handlers
async def cancel_handler(message: types.Message, state: FSMContext):
    """This handler allow cancel any states"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('ОК', reply_markup=default_keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_search_start, commands=['AnimeSearch'])
    dp.register_message_handler(anime_search, state=AnimeSearch.anime_str)
    dp.register_callback_query_handler(characters_page_callback, lambda call: call.data.split('.')[0] == 'anime_founds')

    dp.register_message_handler(mark_anime_start, commands=["AnimeMark"])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    dp.register_message_handler(mark_anime_title, state=MarkAnime.anime_title)
    dp.register_message_handler(mark_anime_status, state=MarkAnime.status)
    dp.register_message_handler(mark_anime_score, state=MarkAnime.score)
