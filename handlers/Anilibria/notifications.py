from aiogram import types
from anilibria import PlaylistUpdate, TitleEpisode

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
    animes = list(map(int, record['animes']))
    animes.remove(id_title)
    DataBase.update_one('user_follows', 'chat_id', message.chat.id, {'animes': animes})

    await message.answer(f"Вы отписались от аниме - <b>{anime_info.names.ru}</b>")


@anilibria_client.listen(name='on_title_episode')
async def send_notification(event: TitleEpisode):
    """Responsible for the delivery of notifications"""
    # Get users follows
    all_users = DataBase.find('user_follows')
    # iteration and check anime in users follows
    for user in all_users:
        if event.title.id in [int(i) for i in user['animes']]:
            await dp.bot.send_photo(user['chat_id'], f"{event.posters.small.full_url}",
                                    caption=f"<i>Вышла Новая Серия</i>"
                                            f"<b>— {event.title.names.ru} | {event.title.names.en}</b>\n"
                                            f"<b>Серия {event.updated_episode.episode}</b>\n\n"
                                            f"<b>Жанры</b>: {', '.join(event.title.genres)}\n"
                                            f"<b>Озвучили</b>: {', '.join(event.title.team.voice)}",
                                    )
