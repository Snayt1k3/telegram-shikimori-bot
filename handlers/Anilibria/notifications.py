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
                               'animes': [],
                               'page': 0})

    record = collection.find_one({'chat_id': message.chat.id})
    ani_l = record['animes'] if record['animes'] is not None else []

    # get info for pretty message
    anime_info = await get_anime_info(id_title)

    if id_title in ani_l:
        await message.answer(f"Вы Уже подписаны на Аниме - {anime_info['names']['ru']}")
        return
    # update user follows
    ani_l.append(id_title)
    collection.update_one({'chat_id': message.chat.id}, {'$set': {'animes': ani_l}})

    await message.answer(f"Вы подписались на Аниме - {anime_info['names']['ru']}")


async def unfollow_notification(id_title: int, message: types.Message):
    # db
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']
    record = collection.find_one({'chat_id': message.chat.id})
    # check user follow anime exists
    if not record['animes']:
        await message.answer('У вас нету ни одного Аниме в подписках')
        return

    collection.update_one({'chat_id': message.chat.id}, {'$set': {'animes': record['animes'].remove(id_title)}})
    anime_info = await get_anime_info(id_title)

    await message.answer(f"Вы отписались от Аниме - {anime_info['names']['ru']}")


async def send_notification():
    pass
