import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink

from Keyboard.keyboard import keyboard_status, default_keyboard, searching_pagination
from bot import dp, db_client
from misc.constants import headers, shiki_url
from .helpful_functions import oauth2_decorator, oauth2_state, get_user_id, get_information_from_anime, \
    check_anime_already_in_profile
from .oauth import check_token
from .validation import check_anime_title, check_user_in_database


class MarkAnime(StatesGroup):
    anime_title = State()
    score = State()
    status = State()


# Anime Search Start

class AnimeSearch(StatesGroup):
    anime_str = State()


async def anime_search_start(message: types.Message):
    """This method a start state AnimeSearch"""
    await AnimeSearch.anime_str.set()
    await message.reply("Write what anime you want to find")


@oauth2_state
async def anime_search(message: types.Message, state: FSMContext):
    """This method make a request, after send 5 anime which found"""
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/animes?search={message.text}&limit=20") as response:
            anime_founds = await response.json()

            # Trash collector
            collection.delete_one({'chat_id': message.chat.id})

            collection.insert_one({"chat_id": message.chat.id,
                                   "anime_founds": anime_founds,
                                   "page": 1})

    await anime_search_pagination(message)
    await state.finish()


@oauth2_decorator
async def anime_search_pagination(message: types.Message):
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]
    record = collection.find_one({"chat_id": message.chat.id})

    anime_founds = record['anime_founds']
    page = record['page']

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=searching_pagination,
                            photo=shiki_url + anime_founds[page - 1]['image']['original'],
                            parse_mode="HTML",
                            caption=f"Anime <b>{page}</b> of <b>{len(anime_founds)}</b> \n "
                                    f"Eng: <b> {anime_founds[page - 1]['name']} </b> \n"
                                    f"Rus: <b> {anime_founds[page - 1]['russian']} </b> \n"
                                    f"Rating: <b> {anime_founds[page - 1]['score']}</b> \n"
                                    f"Episode Count: <b> {anime_founds[page - 1]['episodes']} </b> \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_founds[page - 1]['url'])}"
                            )


async def anime_search_callback(call):
    """this callback implements pagination for function anime_search_pagination"""
    action = call.data.split('.')[1]
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]
    record = collection.find_one({"chat_id": call.message.chat.id})

    if action == "next":
        if record['page'] < len(record['anime_founds']):
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": record['page'] + 1}})
        else:
            await dp.bot.send_message(call.message.chat.id, 'Its last anime which was find')
            return

    elif action == 'previous':
        if record['page'] > 0:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": record['page'] - 1}})
        else:
            await dp.bot.send_message(call.message.chat.id, 'Its first anime which was find')
            return

    elif action == "into_planned":
        id_user = await get_user_id(call.message.chat.id)
        check_anime = await check_anime_already_in_profile(call.message.chat.id,
                                                           record['anime_founds'][record['page'] - 1]['id'])
        if check_anime:
            await dp.bot.send_message(call.message.chat.id,
                                      f"Anime <b>{record['anime_founds'][record['page'] - 1]['name']}</b> Already "
                                      f"Exists in your {check_anime}",
                                      parse_mode='HTML')
            return

        # Mark anime as planned
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(f"{shiki_url}api/v2/user_rates", json={"user_rate": {
                'target_id': record['anime_founds'][record['page'] - 1]['id'],
                'user_id': id_user,
                'target_type': 'Anime',
                'status': 'planned'
            }}) as response:

                if response.status == 201:
                    await dp.bot.delete_message(
                        call.message.chat.id,
                        call.message.message_id
                    )

                    response = await response.json()
                    anime_info = await get_information_from_anime(response['target_id'])
                    await dp.bot.send_message(call.message.chat.id,
                                              f"Anime <b>{anime_info['name']}</b> was added to planned",
                                              parse_mode='HTML')
                # Bad request
                else:
                    await dp.bot.send_message(call.message.chat.id, f"Something went wrong")
                return

    await anime_search_pagination(message=call.message)


# Anime Search End

# Anime Mark Start

async def mark_anime_start(message: types.Message):
    """Start State and asking anime title"""
    # Checking if the user has linked a profile
    if not await check_user_in_database(message.chat.id):
        return

    # Token check
    await check_token()
    await MarkAnime.anime_title.set()
    await message.answer("Hi, enter the exact name of the anime \n\n"
                         "you can cancel - /cancel")


@oauth2_state
async def mark_anime_title(message: types.Message, state: FSMContext):
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


@oauth2_state
async def mark_anime_score(message: types.Message, state: FSMContext):
    """Get Score and Asking Status"""
    async with state.proxy() as data:
        if not message.text.isdigit() or int(message.text) not in [i for i in range(11)]:
            await message.answer('Wrong Rating')
            await state.finish()
        else:
            data['score'] = message.text
            await MarkAnime.next()
            await message.answer("Choose one status", reply_markup=keyboard_status)


@oauth2_state
async def mark_anime_status(message: types.Message, state: FSMContext):
    """Get status and finish State"""
    async with state.proxy() as data:
        id_user = await get_user_id(message.chat.id)

        if message.text in ['completed', 'watching', 'planned', 'rewatching', 'dropped']:
            data['status'] = message.text
            await post_anime_rates(data, id_user)
            await message.answer("Successfully Recorded", reply_markup=default_keyboard)
        else:
            await message.answer("Status is not correct", reply_markup=default_keyboard)

    await state.finish()


@oauth2_decorator
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
    dp.register_callback_query_handler(anime_search_callback, lambda call: call.data.split('.')[0] == 'anime_search')

    dp.register_message_handler(mark_anime_start, commands=["AnimeMark"])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    dp.register_message_handler(mark_anime_title, state=MarkAnime.anime_title)
    dp.register_message_handler(mark_anime_status, state=MarkAnime.status)
    dp.register_message_handler(mark_anime_score, state=MarkAnime.score)
