from aiogram import Dispatcher, types

from Keyboard.inline import cr_kb_by_collection
from bot import db_client
from handlers.translator import translate_text
from .helpful_functions import get_info_anime_from_shiki, add_anime_rate, get_anime_info_user_rate, \
    edit_message_for_view_anime, edit_reply_markup_user_lists, anime_search_edit, delete_anime_from_user_profile, \
    update_anime_eps, display_user_list


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
        kb = cr_kb_by_collection(coll, datas[1], int(datas[2]))
        user_rate = await get_anime_info_user_rate(call.message.chat.id, datas[1])
        anime_info = await get_info_anime_from_shiki(datas[1])
        await edit_message_for_view_anime(call.message, kb, anime_info, user_rate[0])


async def anime_search_callback(call: types.CallbackQuery):
    action = call.data.split('.')[-1]

    if action == 'view':
        await anime_search_edit(call.message, call.data.split('.')[1])

    else:
        await call.message.delete()


async def anime_edit(call: types.CallbackQuery):
    action = call.data.split('.')[-2]
    target_id = call.data.split('.')[1]

    # boring ifs
    if action == 'delete':
        await delete_anime_from_user_profile(target_id, call.message.chat.id)

    elif action == 'complete':
        await add_anime_rate(target_id, call.message.chat.id, 'completed')

    elif action == 'drop':
        await add_anime_rate(target_id, call.message.chat.id, 'dropped')

    elif action == 'watch':
        await add_anime_rate(target_id, call.message.chat.id, 'watching')

    elif action == 'minus':
        info_user_rate = await get_anime_info_user_rate(call.message.chat.id, target_id)
        if info_user_rate[0]['episodes'] == 0:
            await update_anime_eps(target_id, call.message.chat.id, info_user_rate[0]['episodes'] - 1)
        else:
            await call.message.answer(await translate_text(call.message, "You haven't watched a single episode yet"))

    elif action == 'plus':
        info_user_rate = await get_anime_info_user_rate(call.message.chat.id, target_id)
        await update_anime_eps(target_id, call.message.chat.id, info_user_rate[0]['episodes'] + 1)

    else:
        await display_user_list(call.message, call.data.split('.')[0], target_id)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')
    dp.register_callback_query_handler(anime_search_callback, lambda call: call.data.split('.')[0] == 'anime_search')

    dp.register_callback_query_handler(callback_for_user_list, lambda call: call.data.split('.')[-1] == 'user_list')
    dp.register_callback_query_handler(anime_edit, lambda call: call.data.split('.')[-1] == 'anime_edit')
