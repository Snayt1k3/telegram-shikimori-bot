import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink

from Keyboard.inline import inline_kb_tf, watching_keyboard, edit_watching_keyboard, planned_keyboard, edit_planned_keyboard, \
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
    id_user = await get_user_id(message.chat.id)
    db_current = db_client['telegram-shiki-bot']
    animes = await get_animes_by_status_and_id(message.chat.id, 'watching')

    # Get collection for watch_lists
    collection = db_current['anime_watching']
    # trash collector
    collection.delete_many({'id_user': id_user})

    collection.insert_one({"animes": animes,
                           'id_user': id_user,
                           "page": 0})

    await display_anime_on_message(message, 'anime_watching')


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
    id_user = await get_user_id(message.chat.id)
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    # Trash collector
    collection.delete_many({'id_user': id_user})

    animes = await get_animes_by_status_and_id(message.chat.id, 'planned')

    collection.insert_one({'id_user': id_user,
                           "animes": animes,
                           "page": 0})

    await display_anime_on_message(message, 'anime_planned')


async def get_user_completed_list(message: types.Message):
    # get required datas
    id_user = await get_user_id(message.chat.id)
    completed_animes = await get_animes_by_status_and_id(message.chat.id, 'completed')

    # get DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_completed']

    # trash collector
    collection.delete_many({'id_user': id_user})

    # write into db
    collection.insert_one({'id_user': id_user,
                           "animes": completed_animes,
                           'page': 0})

    # call pagination function
    await display_anime_on_message(message, 'anime_completed')


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


async def display_anime_on_message(message: types.Message, coll, is_edit=False):
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]
    record = collection.find_one({'id_user': await get_user_id(message.chat.id)})
    # get datas
    current_anime = record['animes'][record['page']]
    anime_info = await get_information_from_anime(current_anime['target_id'])

    # actions with kb
    kb = completed_keyboard
    if coll == 'anime_watching':
        kb = watching_keyboard
    elif coll == 'anime_planned':
        kb = planned_keyboard

    # if is_edit == True
    if is_edit:
        if coll == 'anime_watching':
            kb = edit_watching_keyboard
        elif coll == 'anime_planned':
            kb = edit_planned_keyboard
        elif coll == 'anime_completed':
            kb = edit_completed_keyboard

    await dp.bot.send_photo(chat_id=message.chat.id,
                            reply_markup=kb,
                            photo=shiki_url + anime_info['image']['original'],
                            parse_mode="HTML",
                            caption=f"<b>Eng</b>: {anime_info['name']}  \n"
                                    f"<b>Rus</b>: {anime_info['russian']} \n"
                                    f"<b>Rating</b>: {anime_info['score']} \n"
                                    f"<b>Your Score</b>: {current_anime['score']} \n"
                                    f"<b>Episode Viewed</b>: {current_anime['episodes']} : {anime_info['episodes']} \n"
                                    f"{hlink('Go to the Anime', shiki_url + anime_info['url'])}"
                            )


def register_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(set_user_nickname, lambda msg: "My Profile" in msg.text)
    dp.register_message_handler(get_user_profile, state=UserNickname.nick)

    dp.register_message_handler(reset_user_profile, lambda msg: "Reset Profile" in msg.text)

    dp.register_message_handler(get_user_watching, lambda msg: "My Watch List" in msg.text)

    dp.register_message_handler(update_score_state, state=UpdateScore.score)

    dp.register_message_handler(get_user_planned, lambda msg: "My Planned List" in msg.text)

    dp.register_message_handler(get_user_completed_list, lambda msg: "My Completed List" in msg.text)

    dp.register_message_handler(update_score_completed_state, state=UpdateScoreCompleted.score)
