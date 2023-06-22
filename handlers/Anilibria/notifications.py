from aiogram import types

from bot import dp
from database.database import DataBase
from misc.constants import ANI_URL
from .helpful_functions import get_anime_info_from_al


async def follow_notification(id_title, message: types.Message):
    """This method add id_title from anilibria.tv, into db"""
    db = DataBase()

    # check user follow anime exists
    if not db.find_one('chat_id', message.chat.id, 'user_follows'):
        db.insert_into_collection('user_follows', {'chat_id': message.chat.id,
                                                   'animes': []})

    # validation animes into record
    record = db.find_one('chat_id', message.chat.id, 'user_follows')
    ani_l = record['animes'] if record['animes'] is not None else []

    # get info for pretty message
    anime_info = await get_anime_info_from_al(id_title)

    if id_title in ani_l:
        await message.answer(f"Вы уже подписаны на Аниме - {anime_info['names']['ru']}")
        return

    # update user follows
    ani_l.append(id_title)
    db.update_one('user_follows', 'chat_id', message.chat.id, {'animes': ani_l})

    await message.answer(f"Вы подписались на Аниме - {anime_info['names']['ru']}")


async def unfollow_notification(id_title: int | str, message: types.Message):
    """This method delete id_title from db"""
    db = DataBase()

    # check user follow anime exists
    record = db.find_one('chat_id', message.chat.id, 'user_follows')

    # check user follow anime exists
    if not record['animes']:
        await message.answer('У вас нету ни одного Аниме в подписках')
        return

    db.update_one('user_follows', 'chat_id', message.chat.id, {'animes': record['animes'].remove(id_title)})
    anime_info = await get_anime_info_from_al(id_title)

    await message.answer(f"Вы отписались от Аниме - {anime_info['names']['ru']}")


async def send_notification(anime_info):

    anime_info = anime_info.json()

    if 'connection' not in anime_info and anime_info['type'] == 'playlist_update':
        ep = anime_info['data']['episode']
        if ep and anime_info['data']['updated_episode']:
            if all(anime_info['data']['updated_episode']['hls'].values()):

                # Get db follow users
                db = DataBase()
                all_users = db.find('user_follows')

                # iteration and check anime in user follows list
                for user in all_users:
                    if anime_info['data']['id'] in user['animes']:
                        anime = await get_anime_info_from_al(anime_info['data']['id'])

                        await dp.bot.send_photo(user['chat_id'], f"{ANI_URL}{anime['posters']['small']['url']}",
                                                parse_mode='HTML',
                                                caption=f"<b>Вышла {ep} Серия </b> — {anime['names']['ru']} - "
                                                        f"{anime['names']['en']}\n\n"
                                                        f"<b>Жанры</b>: {', '.join(anime['genres'])}\n"
                                                        f"<b>Озвучили</b>: {', '.join(anime['team']['voice'])}",
                                                )
