import logging

from aiogram import types
from anilibria import PlaylistUpdate, TitleEpisode

from bot import dp, anilibria_client
from database.animedb import AnimeDB
from misc.constants import ANI_URL


async def follow_notification(title_id: int, message: types.Message) -> None:
    """
    This method, calling db method for add anime subscribe into db
    :param title_id: Anilibria title_id
    :param message: Telegram message
    """

    anime = await AnimeDB.subscribe_notifications(title_id, message.chat.id)

    if anime is None:
        await message.answer("Произошла ошибка, попробуйте еще раз")
    elif isinstance(anime, str):
        await message.answer(anime)
    else:
        await message.answer(f"Вы успешно подписались на аниме - <i>{anime.title_ru}</i>")


async def unfollow_notification(title_id: int, message: types.Message) -> None:
    """
    This method, calling db method for delete anime subscribe from db
    :param title_id: Anilibria title id
    :param message: Telegram msg
    """
    anime = await AnimeDB.unsubscribe_notifications(title_id, message.chat.id)

    if anime is None:
        await message.answer("Произошла ошибка, попробуйте еще раз")
    else:
        await message.answer(f"Вы успешно отписались от аниме - <i> {anime.title_ru} </i>")


@anilibria_client.on(TitleEpisode)
async def send_notification(event: TitleEpisode):
    """Responsible for the delivery of notifications"""
    try:
        # Get all users
        all_users = await AnimeDB.get_all_follows()

        # iteration and check anime in users follows
        for user in all_users:
            if event.title.id in [i.id for i in user.follows]:
                await dp.bot.send_photo(user.chat_id, f"{event.title.posters.small.full_url}",
                                        caption=f"<i>Вышла Новая Серия</i>"
                                                f"<b>— {event.title.names.ru} | {event.title.names.en}</b>\n"
                                                f"<i>Серия {event.episode.episode}</i>\n\n"
                                                f"<b>Жанры</b>: {', '.join(event.title.genres)}\n"
                                                f"<b>Озвучили</b>: {', '.join(event.title.team.voice)}",
                                        )
    except Exception as e:
        logging.error(f"Error occurred when trying to send notifications - {e}")
