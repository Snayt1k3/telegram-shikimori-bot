import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink

from Keyboard.keyboard import inline_kb_tf, watching_pagination, edit_keyboard
from bot import dp, db_client
from .oauth import check_token

headers = {
    'User-Agent': 'Snayt1k3-API',
    'Authorization': 'Bearer Fmz6gr3QscLalIwWMoIrBX7xj78q6-YuxKyjXMrcKuA',
}

shiki_url = "https://shikimori.one/"


class UserNickname(StatesGroup):
    nick = State()


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
        await message.reply("Write your nickname on Shikimori", reply=False)
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


async def reset_user_profile(message: types.Message):
    """If user called this method, her user id will clear"""
    await message.answer("Are You sure?", reply_markup=inline_kb_tf)


async def reset_user_callback(call):
    data = call.data.split(".")
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    if data[1] == "True":
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        collection.delete_one({'chat_id': call.message.chat.id})
        await dp.bot.send_message(call.message.chat.id, "Deleted")
    else:
        await dp.bot.send_message(call.message.chat.id, "Cancelled")


async def get_user_watching(message: types.Message):
    """This method check if user link profile, after """
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["ids_users"]
    if not collection.find_one({'chat_id': message.chat.id}):
        await message.answer("You need to call command /MyProfile and link your nickname")
    else:
        await list_watching_user(message)


async def list_watching_user(message: types.Message):
    """This method get all anime ids and put in database and call method pagination_watching_list"""
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["ids_users"]
    id_user = collection.find_one({'chat_id': message.chat.id})['shikimori_id']
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                shiki_url + f"api/v2/user_rates?status=watching&user_id={id_user}&target_type=Anime") as response:
            anime_ids = []
            anime_ids_del = []
            anime_eps = []
            res = await response.json()
            for anime in res:
                anime_ids.append(anime['target_id'])
                anime_ids_del.append((anime['id']))
                anime_eps.append(anime['episodes'])

            collection = db_current['anime_watch_list']
            collection.delete_one({'chat_id': message.chat.id})
            collection.insert_one({"anime_watch_list_ids": anime_ids,
                                   'chat_id': message.chat.id,
                                   'anime_eps': anime_eps,
                                   "page": 0,
                                   'anime_ids_del': anime_ids_del})
            await pagination_watching_list(message)


async def pagination_watching_list(message: types.message, is_edit=False):
    """This method send page of user watching list"""
    # Db actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_watch_list']
    watch_list = collection.find_one({'chat_id': message.chat.id})
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                shiki_url + f"api/animes/{watch_list['anime_watch_list_ids'][int(watch_list['page'])]}") as response:
            res = await response.json()

            kb = watching_pagination
            if is_edit:
                kb = edit_keyboard

            await dp.bot.send_photo(chat_id=message.chat.id,
                                    reply_markup=kb,
                                    photo=shiki_url + res['image']['original'],
                                    parse_mode="HTML",
                                    caption=f"Eng: <b> {res['name']} </b> \n"
                                            f"Rus: <b> {res['russian']} </b> \n"
                                            f"Rating: <b> {res['score']}</b> \n"
                                            f"Episode Viewed: <b>"
                                            f"{watch_list['anime_eps'][int(watch_list['page'])]}:"
                                            f"{res['episodes']} </b> \n"
                                            f"{hlink('Go to the Anime', shiki_url + res['url'])}"
                                    )


async def anime_watch_callback(call):
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_watch_list']
    watch_list = collection.find_one({"chat_id": call.message.chat.id})
    action = call.data.split('.')[1]

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)

    if action == 'next':
        if len(watch_list['anime_watch_list_ids']) > watch_list['page'] + 1:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": watch_list['page'] + 1}})
            await pagination_watching_list(call.message)
        else:
            await pagination_watching_list(call.message)
            await dp.bot.send_message(call.message.chat.id, "It's last Anime")

    elif action == 'previous':
        if watch_list['page'] > 0:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": watch_list['page'] - 1}})
            await pagination_watching_list(call.message)
        else:
            await pagination_watching_list(call.message)
            await dp.bot.send_message(call.message.chat.id, "It's first anime")
    else:
        await pagination_watching_list(call.message, is_edit=True)


async def callback_watch_anime_edit(call):
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["ids_users"]
    id_user = collection.find_one({'chat_id': call.message.chat.id})['shikimori_id']

    collection = db_current['anime_watch_list']

    watch_list = collection.find_one({"chat_id": call.message.chat.id})

    action = call.data.split(".")[1]
    if action == 'back':
        await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
        await pagination_watching_list(call.message, is_edit=False)

    if action == 'delete':
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(shiki_url + f"api/v2/user_rates/" +
                                      f"{watch_list['anime_ids_del'][int(watch_list['page'])]}",
                                      json={
                                          "user_rate": {
                                              "user_id": id_user,
                                              "target_type": "Anime"
                                          }
                                      }) as response:

                if response.status == 204:
                    await dp.bot.send_message(call.message.chat.id, f"Anime Was Deleted")
                else:
                    await dp.bot.send_message(call.message.chat.id, "Error")

    if action == 'minus' or 'add':
        ep = watch_list['anime_eps'][int(watch_list['page'])]

        if action == 'minus':
            ep -= 1

        elif action == 'add':
            ep += 1

        watch_list['anime_eps'][int(watch_list['page'])] = ep
        collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"anime_eps": watch_list['anime_eps']}})

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.patch(
                    shiki_url + f"api/v2/user_rates/{watch_list['anime_ids_del'][int(watch_list['page'])]}",
                    json={"user_rate": {
                        "user_id": id_user,
                        "target_type": "Anime",
                        "episodes": ep
                    }}) as response:

                if response.status == 200:
                    res = await response.json()
                    await dp.bot.send_message(call.message.chat.id, f"Anime Updated, current eps - {res['episodes']}")
                else:
                    await dp.bot.send_message(call.message.chat.id, 'Something went wrong')

        await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
        await pagination_watching_list(call.message, is_edit=True)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(set_user_nickname, commands=['MyProfile'])
    dp.register_message_handler(get_user_profile, state=UserNickname.nick)

    dp.register_message_handler(reset_user_profile, commands=['ResetProfile'])
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')

    dp.register_message_handler(get_user_watching, commands=['MyWatchList'])
    dp.register_callback_query_handler(anime_watch_callback, lambda call: call.data.split('.')[0] == 'anime_watch')
    dp.register_callback_query_handler(callback_watch_anime_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_watch_one')
