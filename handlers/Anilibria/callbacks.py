from aiogram import types, Dispatcher

from bot import db_client
from .other_functional import display_anime_al, edit_anime_al


async def paginator_callback(call: types.CallbackQuery):
    action = call.data.split('.')[2]
    coll = call.data.split('.')[1]

    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]
    record = collection.find_one({'chat_id': call.message.chat.id})
    page = record['page']

    # Validation
    if action == 'prev':
        if page - 1 > 0:
            page -= 1
        else:
            await call.message.answer("Это первое Аниме, Которое было найдено")
            return

    elif action == 'next':
        if page + 1 < len(record['animes']):
            page += 1
        else:
            await call.message.answer("Это Последнее Аниме, Которое было найдено")
            return

    collection.update_one({'chat_id': call.message.chat.id}, {'$set': {'page': page}})
    await edit_anime_al(call.message, coll)


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(paginator_callback, lambda call: call.data.split('.')[0] == 'paginator_al')
