import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from telegram_bot_pagination import InlineKeyboardPaginator

from Keyboard.keyboard import keyboard_status, keyboard_cancel
from bot import dp, db_client
from .oauth import check_token

headers = {
    'User-Agent': 'Snayt1k3',
    'Authorization': 'Bearer GaX9DsIVqRd_bJSyGCA0Y3pxZTZq5ZLx472vfRkKfUg',
}

shiki_url = "https://shikimori.one/"


class AnimeSearch(StatesGroup):
    anime_str = State()


class MarkAnime(StatesGroup):
    anime_title = State()
    score = State()
    status = State()


class UserNickname(StatesGroup):
    nick = State()


async def anime_search_start(message: types.Message):
    # Token check
    await check_token()

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


async def check_anime_title(title):
    """Validation Anime Title"""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/animes?search={title}&limit=5") as response:
            anime_founds = await response.json()
            if anime_founds:
                return anime_founds[0]


async def cancel_handler(message: types.Message, state: FSMContext):
    """Cancel Handler"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('ОК')


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
        if not anime:
            await state.finish()
            await message.answer('Anime not found')
        else:
            await dp.bot.send_photo(chat_id=message.chat.id,
                                    reply_markup=paginator.markup,
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
        if message.text in ['completed', 'watching', 'planned', 'rewatching', 'dropped']:
            data['status'] = message.text
            await post_anime_rates(data)
            await message.answer("Successfully Recorded")
        else:
            await message.answer("Status is not correct")

    await state.finish()


async def post_anime_rates(anime_data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
                "https://shikimori.one/api/v2/user_rates", json={
                    "user_rate": {
                        "score": anime_data['score'],
                        "status": anime_data['status'],
                        "target_id": anime_data['anime']['id'],
                        "target_type": "Anime",
                        "user_id": '1020660',
                    }
                }) as response:
            print(response)
            print(await response.text())


async def set_user_nickname(message: types.message):
    """If user call command /GetProfile first time, we add user id into db
    else call method user_profile Which send user profile"""

    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["ids_users"]

    # Token check
    await check_token()

    if not collection.find_one({'chat_id': message.chat.id}):
        await UserNickname.nick.set()
        await message.reply("Write your nickname on Shikimori")
    else:
        await user_profile(message)


async def user_profile(message: types):
    async with aiohttp.ClientSession(headers=headers) as session:
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        id = collection.find_one({'chat_id': message.chat.id})
        async with session.get(f"https://shikimori.one/api/users/{id['shikimori_id']}") as response:

            res = await response.json()
            animes = res['stats']['statuses']['anime']

            await message.answer(f"Your Profile\n" + f"Nickname: <b>{res['nickname']}</b>\n"
                                 + f"Your id: {res['id']}\n"
                                 + f"{animes[0]['name']} - {animes[0]['size']}\n"
                                 + f"{animes[1]['name']} - {animes[1]['size']}\n"
                                 + f"{animes[2]['name']} - {animes[2]['size']}\n"
                                 + f"{animes[4]['name']} - {animes[4]['size']}\n"
                                 + f"{hlink('Go to my Profile', shiki_url + res['nickname'])}",
                                 parse_mode="HTML")


async def get_user_profile(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/users/{message.text}?is_nickname=1") as response:
            res = await response.json()
            if response.status == 404:
                await message.answer("Your Profile Not found")

            else:
                # Db connect
                db_current = db_client['telegram-shiki-bot']
                # get collection
                collection = db_current["ids_users"]
                # insert
                if not collection.find_one({'chat_id': message.chat.id}):
                    collection.insert_one({"chat_id": message.chat.id,
                                           "shikimori_id": res['id']})

                animes = res['stats']['statuses']['anime']
                await message.answer(f"Your Profile\n" + f"Nickname: <b>{res['nickname']}</b>\n"
                                     + f"Your id: {res['id']}\n"
                                     + f"{animes[0]['name']} - {animes[0]['size']}\n"
                                     + f"{animes[1]['name']} - {animes[1]['size']}\n"
                                     + f"{animes[2]['name']} - {animes[2]['size']}\n"
                                     + f"{animes[4]['name']} - {animes[4]['size']}\n"
                                     + f"{hlink('Go to my Profile', shiki_url + res['nickname'])}",
                                     parse_mode="HTML")
            await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(anime_search_start, commands=['AnimeSearch'])
    dp.register_message_handler(anime_search, state=AnimeSearch.anime_str)
    dp.register_callback_query_handler(characters_page_callback, lambda call: call.data.split('.')[0] == 'anime_founds')

    dp.register_message_handler(mark_anime_start, commands=["MarkAnime"])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    dp.register_message_handler(mark_anime_title, state=MarkAnime.anime_title)
    dp.register_message_handler(mark_anime_status, state=MarkAnime.status)
    dp.register_message_handler(mark_anime_score, state=MarkAnime.score)

    dp.register_message_handler(set_user_nickname, commands=['GetProfile'])
    dp.register_message_handler(get_user_profile, state=UserNickname.nick)
