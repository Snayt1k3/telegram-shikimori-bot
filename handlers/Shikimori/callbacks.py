from aiogram import Dispatcher, types

from Keyboard.inline import cr_kb_by_collection
from bot import db_client
from handlers.translator import translate_text
from .helpful_functions import get_info_anime_from_shiki, add_anime_rate, \
    get_anime_info_user_rate, edit_message_for_view_anime, \
    edit_reply_markup_user_lists


async def reset_user_callback(call: types.CallbackQuery):
    # get choose user
    data = call.data.split(".")[1]

    if data == "True":
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        collection.delete_one({'chat_id': call.message.chat.id})
        await call.message.answer(await translate_text(call.message, "Deleted"))
    else:
        await call.message.answer(await translate_text(call.message, "❌ Cancelled"))

    await call.message.delete()


async def anime_search_callback(call: types.CallbackQuery):
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
            await call.message.answer(await translate_text(call.message, 'Its last anime which was find'))
            return

    elif action == 'previous':
        if record['page'] > 0:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": record['page'] - 1}})
        else:
            await call.message.answer(await translate_text(call.message, 'Its first anime which was find'))
            return

    elif action == "into_planned":
        check_anime = await check_anime_already_in_profile(call.message.chat.id,
                                                           record['anime_founds'][record['page'] - 1]['id'])
        if check_anime:
            await call.message.answer(f"Anime <b>{record['anime_founds'][record['page'] - 1]['name']}</b> "
                                      f"{await translate_text(call.message, 'Already')} "
                                      f"{await translate_text(call.message, f'Exists in your {check_anime}')}",
                                      parse_mode='HTML')
            return

        # Mark anime as planned
        res = await add_anime_rate(record['anime_founds'][record['page'] - 1]['id'], call.message.chat.id,
                                   'completed')
        if res.status == 201:
            await call.message.delete()

            await call.message.answer(await translate_text(call.message, "Anime was added to planned"),
                                      parse_mode='HTML')
        # Bad request
        else:
            await call.message.answer(await translate_text(call.message, "Something went wrong"))
        return

    await anime_search_pagination(call.message)
    await call.message.delete()


async def callback_for_user_list(call: types.CallbackQuery):
    datas = call.data.split('.')
    action = datas[3]
    coll = datas[0]

    if action == 'next':
        await edit_reply_markup_user_lists(call.message, coll, "+", int(datas[2]))

    elif action == 'prev':
        await edit_reply_markup_user_lists(call.message, coll, "-", int(datas[2]))

    else:
        # action == 'view'
        kb = cr_kb_by_collection(coll, datas[1])
        user_rate = await get_anime_info_user_rate(call.message.chat.id, datas[1])
        anime_info = await get_info_anime_from_shiki(datas[1])
        await edit_message_for_view_anime(call.message, kb, anime_info, user_rate[0])


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')
    dp.register_callback_query_handler(anime_search_callback, lambda call: call.data.split('.')[0] == 'anime_search')

    dp.register_callback_query_handler(callback_for_user_list, lambda call: call.data.split('.')[-1] == 'user_list')
