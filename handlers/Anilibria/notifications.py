from aiogram import types

from bot import db_client
from .other_functional import get_anime_info


async def follow_notification(id_title: int, message: types.Message):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']

    # check user follow anime exists
    if not collection.find_one({'chat_id': message.chat.id}):
        collection.insert_one({'chat_id': message.chat.id,
                               'animes': []})

    record = collection.find_one({'chat_id': message.chat.id})

    ani_l = record['animes'] if record['animes'] else []
    collection.update_one({'chat_id': message.chat.id}, {'$set': {'animes': ani_l.append(id_title)}})
    anime_info = await get_anime_info(id_title)

    await message.answer(f"Вы подписались на Аниме - {anime_info['name']['ru']}")


async def unfollow_notification(id_title: int, message: types.Message):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']

    # check user follow anime exists
    if not collection.find_one({'chat_id': message.chat.id}):
        await message.answer('У вас нету ни одного Аниме в подписках')
        return

    record = collection.find_one({'chat_id': message.chat.id})

    collection.update_one({'chat_id': message.chat.id}, {'$set': {'animes': record['animes'].remove(id_title)}})
    anime_info = await get_anime_info(id_title)

    await message.answer(f"Вы отписались от Аниме - {anime_info['name']['ru']}")


async def send_notification():
    pass