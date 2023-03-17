from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.inline import cr_kb_by_collection
from bot import db_client, dp
from handlers.translator import translate_text
from .helpful_functions import get_info_anime_from_shiki, add_anime_rate, get_anime_info_user_rate, \
    edit_message_for_view_anime, edit_reply_markup_user_lists, anime_search_edit, delete_anime_from_user_profile, \
    update_anime_eps, display_user_list, update_anime_score, anime_search_edit_back


async def reset_user_callback(call: types.CallbackQuery):
    # get choose user
    data = call.data.split(".")[1]

    if data == "True":
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        collection.delete_one({'chat_id': call.message.chat.id})
        await call.message.answer(await translate_text(call.message, "☑️ Deleted"))
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
        await call.message.answer(await translate_text(call.message, f'Anime was deleted from your profile'))
        await call.message.delete()

    elif action == 'complete':
        await add_anime_rate(target_id, call.message.chat.id, 'completed')
        await call.message.answer(await translate_text(call.message, f'Anime was added to completed list'))
        await call.message.delete()

    elif action == 'drop':
        await add_anime_rate(target_id, call.message.chat.id, 'dropped')
        await call.message.answer(await translate_text(call.message, f'Anime was added to dropped list'))
        await call.message.delete()

    elif action == 'watch':
        await add_anime_rate(target_id, call.message.chat.id, 'watching')
        await call.message.answer(await translate_text(call.message, f'Anime was added to watching list'))
        await call.message.delete()

    elif action == 'minus':
        info_user_rate = await get_anime_info_user_rate(call.message.chat.id, target_id)
        if info_user_rate[0]['episodes'] > 0:
            res = await update_anime_eps(target_id, call.message.chat.id, info_user_rate[0]['episodes'] - 1)
            await call.message.answer(await translate_text(call.message, f'Anime episodes has been updated, '
                                                                         f'current episodes - {res["episodes"]}'))
        else:
            await call.message.answer(await translate_text(call.message, "You haven't watched a single episode yet"))

    elif action == 'plus':
        info_user_rate = await get_anime_info_user_rate(call.message.chat.id, target_id)
        res = await update_anime_eps(target_id, call.message.chat.id, info_user_rate[0]['episodes'] + 1)
        await call.message.answer(await translate_text(call.message, f'Anime episodes has been updated, '
                                                                     f'current episodes - {res["episodes"]}'))

    elif action == 'back':
        await display_user_list(call.message, call.data.split('.')[0], target_id)

    else:
        # create kb rating 0-10
        kb = InlineKeyboardMarkup(row_width=5)
        btns = [InlineKeyboardButton(text=f'{i}', callback_data=f"{i}.{target_id}.update_score")
                for i in range(0, 11)]

        kb.row(btns[0], btns[1], btns[2], btns[3], btns[4])
        kb.row(btns[5], btns[6], btns[7], btns[8], btns[9])

        kb.add(InlineKeyboardButton('❌ Cancel', callback_data="cancel.update_score"))
        await dp.bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          reply_markup=kb,
                                          caption="📃 Select Rating")


async def update_score(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    if action == 'cancel':
        await call.message.delete()

    else:

        res = await update_anime_score(call.data.split('.')[1], call.message.chat.id, action)
        await call.message.delete()
        await call.message.answer(await translate_text(call.message, f'Anime score has been updated, '
                                                                     f'current score - {res["score"]}'))


async def anime_search_edit_callback(call: types.CallbackQuery):
    action = call.data.split('.')[-1]
    target_id = call.data.split('.')[1]

    if action == 'completed' or action == 'planned':
        await add_anime_rate(target_id, call.message.chat.id, action)
        await call.message.answer(await translate_text(call.message,
                                                       f"Anime has been added to your {action} list"))
        await call.message.delete()

    else:
        await anime_search_edit_back(call.message)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')
    dp.register_callback_query_handler(anime_search_callback, lambda call: call.data.split('.')[0] == 'anime_search')
    dp.register_callback_query_handler(anime_search_edit_callback,
                                       lambda call: call.data.split('.')[0] == 'anime_search_edit')

    dp.register_callback_query_handler(callback_for_user_list, lambda call: call.data.split('.')[-1] == 'user_list')
    dp.register_callback_query_handler(anime_edit, lambda call: call.data.split('.')[-1] == 'anime_edit')

    dp.register_callback_query_handler(update_score, lambda call: call.data.split('.')[-1] == 'update_score')
