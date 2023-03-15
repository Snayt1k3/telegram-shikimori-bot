import json
import random

from aiogram import types

from bot import db_client, dp
from .helpful_functions import get_anime_info
from aiogram import types
from misc.constants import ani_url

async def follow_notification(id_title: int, message: types.Message):
    """This method add id_title from anilibria.tv, into db"""
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['user_follows']
    # check user follow anime exists
    if not collection.find_one({'chat_id': message.chat.id}):
        collection.insert_one({'chat_id': message.chat.id,
                               'animes': []})

    # validation animes into record
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
    """This method delete id_title from db"""
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


async def send_notification(anime_info):

    if 'connection' not in anime_info and anime_info['type'] == 'playlist_update':
        ep = anime_info['data']['episode']
        if ep and anime_info['data']['updated_episode']:
            if anime_info['data']['updated_episode']['hls']['fhd']:

                # Get db follow users
                db = db_client['telegram-shiki-bot']
                coll = db['user_follows']
                all_users = coll.find()

                # iteration and check anime in user follows list
                for user in all_users:
                    if anime_info['data']['id'] in user['animes']:

                        anime = await get_anime_info(anime_info['data']['id'])

                        await dp.bot.send_photo(user['chat_id'], f"{ani_url}{anime['posters']['small']['url']}",
                                                parse_mode='HTML',
                                                caption=f"<b>Вышла Серия {ep}</b> — {anime['names']['ru']} - "
                                                        f"{anime['names']['en']}\n\n"
                                                        f"<b>Жанры</b>: {', '.join(anime['genres'])}\n"
                                                        f"<b>Озвучили</b>: {', '.join(anime['team']['voice'])}",
                                                )
