import logging

from aiogram import types
from anilibria import PlaylistUpdate, TitleEpisode

from bot import dp, anilibria_client
from database.animedb import AnimeDB
from misc.constants import ANI_URL


async def follow_notification(title_id: int, call: types.CallbackQuery) -> None:
    """
    This method, calling db method for add anime subscribe into db
    :param title_id: Anilibria title_id
    :param call: Telegram call message
    """

    anime = await AnimeDB.subscribe_notifications(title_id, call.message.chat.id)

    if anime is None:
        await call.answer("Произошла ошибка, попробуйте еще раз")
    elif isinstance(anime, str):
        await call.answer(anime)
    else:
        await call.answer(
            f"Вы подписались на уведомления о выходе новых серий аниме '{anime.title_ru}'"
        )


async def unfollow_notification(title_id: int, call: types.CallbackQuery) -> None:
    """
    This method, calling db method for delete anime subscribe from db
    :param title_id: Anilibria title id
    :param call: Telegram call msg
    """
    anime = await AnimeDB.unsubscribe_notifications(title_id, call.message.chat.id)

    if anime is None:
        await call.answer("Произошла ошибка, попробуйте еще раз")
    else:
        await call.answer(
            f"Вы больше не будете получать уведомления о выходе новых серий аниме '{anime.title_ru}'."
        )


@anilibria_client.on(TitleEpisode)
async def send_notification(event: TitleEpisode):
    """Responsible for the delivery of notifications"""
    try:
        print("Follows")
        # Get all users
        all_users = await AnimeDB.get_all_follows()

        # iteration and check anime in users follows
        for user in all_users:
            if event.title.id in [i.id for i in user.follows]:
                await dp.bot.send_photo(
                    user.chat_id,
                    f"{event.title.posters.small.full_url}",
                    caption=f"<b>{event.title.names.ru} | {event.title.names.en}</b>\n"
                    f"<i>Новая серия уже доступна!</i>\n"
                    f"<i>Серия {event.episode.episode}</i>\n\n"
                    f"Пусть каждый момент увлечёт вас в захватывающее путешествие, "
                    f"а герои вдохновят на новые свершения. Наслаждайтесь просмотром! 🌟🚀📺\n",
                )
    except Exception as e:
        logging.error(f"Error occurred when trying to send notifications - {e}")
