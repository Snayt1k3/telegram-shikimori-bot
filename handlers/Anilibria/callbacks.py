from aiogram import types, Dispatcher

from bot import db_client
from .notifications import follow_notification, unfollow_notification
from .other_functional import edit_anime_al


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


async def follow_unfollow_callback(call: types.CallbackQuery):
    coll = call.data.split('.')[1]
    action = call.data.split('.')[2]

    # search into db
    db = db_client['telegram-shiki-bot']
    collection = db[coll]
    record = collection.find_one({'chat_id': call.message.chat.id})

    title = record['animes'][record['page']]

    if coll != 'user_follows':
        title = title['id']

    if action == 'follow':
        await follow_notification(title, call.message)
    else:
        await unfollow_notification(title, call.message)

    await call.message.delete()


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(paginator_callback, lambda call: call.data.split('.')[0] == 'paginator_al')
    dp.register_callback_query_handler(follow_unfollow_callback,
                                       lambda call: call.data.split('.')[0] == 'anilibria_follow')
