from aiogram import types
from anilibria.client.client import PlaylistUpdate

from bot import dp, anilibria_client
from database.database import DataBase
from misc.constants import ANI_URL


async def follow_notification(id_title: int, message: types.Message):
    """This method add id_title from anilibria.tv, into db"""

    # check user follow anime exists
    if not DataBase.find_one('chat_id', message.chat.id, 'user_follows'):
        DataBase.insert_into_collection('user_follows', {'chat_id': message.chat.id, 'animes': []})

    # validation animes into record
    record = DataBase.find_one('chat_id', message.chat.id, 'user_follows')
    ls = record['animes'] if record['animes'] is not None else []

    # get info for pretty message
    anime_info = await anilibria_client.get_title(id=id_title)

    if id_title in ls:
        await message.answer(f"Вы уже подписаны на аниме - <b>{anime_info.names.ru}</b>")
        return

    # update user follows
    ls.append(id_title)
    DataBase.update_one('user_follows', 'chat_id', message.chat.id, {'animes': ls})

    await message.answer(f"Вы подписались на аниме - <b>{anime_info.names.ru}</b>")


async def unfollow_notification(id_title: int, message: types.Message):
    """This method delete id_title from db"""
    record = DataBase.find_one('chat_id', message.chat.id, 'user_follows')

    # check user follow anime exists
    if not record['animes']:
        await message.answer('У вас нету ни одного аниме в подписках')
        return

    anime_info = await anilibria_client.get_title(id=id_title)
    record['animes'].remove(id_title)
    DataBase.update_one('user_follows', 'chat_id', message.chat.id, {'animes': record['animes']})

    await message.answer(f"Вы отписались от аниме - <b>{anime_info.names.ru}</b>")


@anilibria_client.on(PlaylistUpdate)
async def send_notification(event: PlaylistUpdate):
    """Responsible for the delivery of notifications"""
    # Get users follows
    all_users = DataBase.find('user_follows')
    anime = await anilibria_client.get_title(id=event.id)

    # iteration and check anime in users follows
    for user in all_users:
        if event.id in user['animes']:
            await dp.bot.send_photo(user['chat_id'], f"{ANI_URL + anime.posters.small.url}",
                                    caption=f"<b>Вышла {event.updated_episode.episode} Серия </b>"
                                            f"— {anime.names.ru} | {anime.names.en}\n\n"
                                            f"<b>Жанры</b>: {', '.join(anime.genres)}\n"
                                            f"<b>Озвучили</b>: {', '.join(anime.team.voice)}",
                                    )
