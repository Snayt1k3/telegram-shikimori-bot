import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from Keyboard.inline import inline_kb_tf, watching_pagination, edit_keyboard, planned_keyboard, edit_planned_keyboard, \
    completed_keyboard, edit_completed_keyboard
from bot import dp, db_client
from misc.constants import headers, shiki_url
from .helpful_functions import get_information_from_anime, get_user_id, oauth2, get_animes_by_status_and_id, \
    update_anime_score, get_anime_info_user_rate
from .states import UpdateScore, UserNickname, UpdateScoreCompleted
from .validation import check_user_in_database


async def set_user_nickname(message: types.Message):
    """If user call command /GetProfile first time, we add user id into db
    else call method user_profile Which send user profile"""

    user_id = await get_user_id(message.chat.id)
    # here check if user already have nick from shiki
    if not user_id:
        await UserNickname.nick.set()
        await message.reply("Write your nickname on Shikimori", reply=False)
    else:
        await user_profile(message)


@oauth2
async def user_profile(message: types.Message):
    """This method send a user profile and information from profile"""
    async with aiohttp.ClientSession(headers=headers) as session:
        user_id = await get_user_id(message.chat.id)
        async with session.get(f"{shiki_url}api/users/{user_id}") as response:
            res = await response.json()
            anime_stats = res['stats']['statuses']['anime']

            await message.answer(f"Your Profile\n" + f"Nickname: <b>{res['nickname']}</b>\n"
                                 + f"Your id: {res['id']}\n"
                                 + f"{anime_stats[0]['name']} - {anime_stats[0]['size']}\n"
                                 + f"{anime_stats[1]['name']} - {anime_stats[1]['size']}\n"
                                 + f"{anime_stats[2]['name']} - {anime_stats[2]['size']}\n"
                                 + f"{anime_stats[4]['name']} - {anime_stats[4]['size']}\n"
                                 + f"{hlink('Go to my Profile', shiki_url + res['nickname'])}",
                                 parse_mode="HTML")


async def get_user_profile(message: types.Message, state: FSMContext):
    """This method call, when user call first time MyProfile and set nickname if found """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{shiki_url}api/users/{message.text}?is_nickname=1") as response:
            res = await response.json()
            if response.status == 404:
                await message.answer("Your Profile Not found")

            else:
                # Db connect
                db_current = db_client['telegram-shiki-bot']
                # get collection ids_users
                collection = db_current["ids_users"]
                # insert one record
                if not collection.find_one({'chat_id': message.chat.id}):
                    collection.insert_one({"chat_id": message.chat.id,
                                           "shikimori_id": res['id']})

                anime_stats = res['stats']['statuses']['anime']
                await message.answer(f"Your Profile\n" + f"Nickname: <b>{res['nickname']}</b>\n"
                                     + f"Your id: {res['id']}\n"
                                     + f"{anime_stats[0]['name']} - {anime_stats[0]['size']}\n"
                                     + f"{anime_stats[1]['name']} - {anime_stats[1]['size']}\n"
                                     + f"{anime_stats[2]['name']} - {anime_stats[2]['size']}\n"
                                     + f"{anime_stats[4]['name']} - {anime_stats[4]['size']}\n"
                                     + f"{hlink('Go to my Profile', shiki_url + res['nickname'])}",
                                     parse_mode="HTML")
            await state.finish()


async def reset_user_profile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer("Are You sure?", reply_markup=inline_kb_tf)


async def get_user_watching(message: types.Message):
    """This method check if user link profile """

    if not await check_user_in_database(message.chat.id):
        return

    await list_watching_user(message)


@oauth2
async def list_watching_user(message: types.Message):
    """This method get all anime ids and put in database and call method pagination_watching_list"""
    db_current = db_client['telegram-shiki-bot']
    user_watch_list = await get_animes_by_status_and_id(message.chat.id, 'watching')
    anime_target_ids = []

    for anime in user_watch_list:
        anime_target_ids.append(anime['target_id'])

    # Get collection for watch_lists
    collection = db_current['anime_watch_list']
    # trash collector
    collection.delete_many({'chat_id': message.chat.id})

    collection.insert_one({"anime_target_ids": anime_target_ids,
                           'chat_id': message.chat.id,
                           "page": 0})

    await pagination_watching_list(message)


@oauth2
async def pagination_watching_list(message: types.Message, is_edit=False):
    """This method send page of user watching list"""
    # Db actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_watch_list']
    watch_list = collection.find_one({'chat_id': message.chat.id})
    # Make a request with helpful function
    anime_info = await get_information_from_anime(watch_list['anime_target_ids'][watch_list['page']])
    # get info user rate
    info_user_rate = await get_anime_info_user_rate(message.chat.id, watch_list['anime_target_ids'][watch_list['page']])

    # Depends on is_edit, this kb implements edit anime
    kb = watching_pagination
    if is_edit:
        kb = edit_keyboard

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=kb,
                            photo=shiki_url + anime_info['image']['original'],
                            parse_mode="HTML",
                            caption=f"<b>Eng</b>: {anime_info['name']}  \n"
                                    f"<b>Rus</b>: {anime_info['russian']} \n"
                                    f"<b>Rating</b>: {anime_info['score']} \n"
                                    f"<b>Your Score</b>: {info_user_rate[0]['score']} \n"
                                    f"<b>Episode Viewed</b>: {info_user_rate[0]['episodes']}:{anime_info['episodes']} \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_info['url'])}"
                            )


async def update_score_state(message: types.Message, state: FSMContext):
    await state.finish()

    if not int(message.text) in range(1, 11):
        await dp.bot.send_message(message.chat.id, f"❌ Write a correctly score")
        return

    # DB actions
    db_current = db_client['telegram-shiki-bot']

    # Change collection, for actions on anime
    collection = db_current['anime_watch_list']

    # get data
    watch_list = collection.find_one({"chat_id": message.chat.id})
    res = await update_anime_score(watch_list['anime_target_ids'][watch_list['page']], message.chat.id, message.text)

    if res:
        await dp.bot.send_message(message.chat.id, f"✔️ Anime Successfully updated")

    else:
        await dp.bot.send_message(message.chat.id, f"❌ Something went wrong")


async def get_user_planned(message: types.Message):
    """This function Basically doing actions with the database"""
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    # Trash collector
    collection.delete_many({'chat_id': message.chat.id})

    animes = await get_animes_by_status_and_id(message.chat.id, 'planned')

    collection.insert_one({'chat_id': message.chat.id,
                           "animes": animes,
                           "page": 0})

    await paginator_planned_list(message)


async def paginator_planned_list(message: types.Message, is_edit=False):
    """This function paginator for user planned list """
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    record = collection.find_one({"chat_id": message.chat.id})

    # get require datas
    current_anime = record["animes"][record['page']]
    anime_info = await get_information_from_anime(current_anime['target_id'])

    # Keyboard actions
    kb = planned_keyboard
    if is_edit:
        kb = edit_planned_keyboard

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=kb,
                            photo=shiki_url + anime_info['image']['original'],
                            parse_mode="HTML",
                            caption=f"Anime <b>{record['page'] + 1}</b> of <b>{len(record['animes'])}</b> \n"
                                    f"Eng: <b> {anime_info['name']} </b> \n"
                                    f"Rus: <b> {anime_info['russian']} </b> \n"
                                    f"Rating: <b> {anime_info['score']}</b> \n"
                                    f"Episodes: <b>{anime_info['episodes']}</b> \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_info['url'])}"
                            )


async def get_user_completed_list(message: types.Message):
    # get required datas
    id_user = await get_user_id(message.chat.id)
    completed_animes = await get_animes_by_status_and_id(message.chat.id, 'completed')

    # get DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_completed']
    collection.delete_many({'id_user': id_user})

    # write into db
    collection.insert_one({'id_user': id_user,
                           "completed_animes": completed_animes,
                           'page': 0})

    # call pagination function
    await paginator_completed_list(message)


async def paginator_completed_list(message: types.Message, is_edit=False):
    # get required datas
    id_user = await get_user_id(message.chat.id)

    # get DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_completed']
    completed_animes = collection.find_one({'id_user': id_user})

    anime_with_page = completed_animes['completed_animes'][completed_animes['page']]

    anime_info = await get_information_from_anime(
        anime_with_page['target_id']
    )

    kb = completed_keyboard
    if is_edit:
        kb = edit_completed_keyboard

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=kb,
                            photo=shiki_url + anime_info['image']['original'],
                            parse_mode="HTML",
                            caption=f"<b>Eng</b>: {anime_info['name']}  \n"
                                    f"<b>Rus</b>: {anime_info['russian']} \n"
                                    f"<b>Rating</b>: {anime_info['score']} \n"
                                    f"<b>Your Score</b>: {anime_with_page['score']} \n"
                                    f"<b>Episode Viewed</b>: {anime_with_page['episodes']}:{anime_info['episodes']} \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_info['url'])}"
                            )


async def update_score_completed_state(message: types.Message, state: FSMContext):
    await state.finish()

    if not int(message.text) in range(1, 11):
        await dp.bot.send_message(message.chat.id, f"❌ Write a correctly score")
        return

    # DB actions
    db_current = db_client['telegram-shiki-bot']

    # Change collection, for actions on anime
    collection = db_current['anime_completed']

    # get data
    id_user = await get_user_id(message.chat.id)

    completed_animes = collection.find_one({"id_user": id_user})
    anime_with_page = completed_animes['completed_animes'][completed_animes['page']]
    res = await update_anime_score(anime_with_page['target_id'], message.chat.id, message.text)

    if res:
        await dp.bot.send_message(message.chat.id, f"✔️ Anime Successfully updated")

    else:
        await dp.bot.send_message(message.chat.id, f"❌ Something went wrong")


def register_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(set_user_nickname, lambda msg: "My Profile" in msg.text)
    dp.register_message_handler(get_user_profile, state=UserNickname.nick)

    dp.register_message_handler(reset_user_profile, lambda msg: "Reset Profile" in msg.text)

    dp.register_message_handler(get_user_watching, lambda msg: "My Watch List" in msg.text)

    dp.register_message_handler(update_score_state, state=UpdateScore.score)

    dp.register_message_handler(get_user_planned, lambda msg: "My Planned List" in msg.text)

    dp.register_message_handler(get_user_completed_list, lambda msg: "My Completed List" in msg.text)

    dp.register_message_handler(update_score_completed_state, state=UpdateScoreCompleted.score)
