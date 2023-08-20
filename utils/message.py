import logging

from aiogram.utils.markdown import hlink
from anilibria import TitleEpisode

from misc.constants import SHIKI_URL


class Message:
    """
    Class, makes message to format we need
    """

    async def notification_msg(self, event: TitleEpisode) -> str:
        """Creates a notification message"""
        try:
            msg = (
                f"<b>{event.title.names.ru} | {event.title.names.en}</b>\n"
                f"<i>Новая серия уже доступна!</i>\n"
                f"<i>Серия {event.episode.episode}</i>\n\n"
                f"Пусть каждый момент увлечёт вас в захватывающее путешествие, "
                f"а герои вдохновят на новые свершения. Наслаждайтесь просмотром! 🌟🚀📺\n",
            )
            return msg
        except Exception as e:
            logging.error(f"Error occurred while forming notifications message - {e}")

    async def profile_msg(self, profile: dict) -> str:
        """create a profile message"""
        try:
            anime_stats = profile["stats"]["statuses"]["anime"]
            msg = (
                f"Никнейм - {hlink(profile['nickname'], SHIKI_URL + profile['nickname'])}\n\n"
                f"Ваши списки на Shikimori:\n"
                f"• <i>Запланированное</i> - {anime_stats[0]['size']}\n"
                f"• <i>Смотрю</i> - {anime_stats[1]['size']}\n"
                f"• <i>Просмотрено</i> - {anime_stats[2]['size']}\n"
                f"• <i>Брошено</i> - {anime_stats[4]['size']}\n\n"
                "Продолжай наслаждаться аниме миром и приятных просмотров! 📺🌟"
            )

            return msg

        except Exception as e:
            logging.error(f"Error occurred while create profile msg - {e}")

    async def anime_info_rate_msg(self, user_rate: dict, anime_info: dict) -> str:
        """
        create a message for anime info by user_rate
        :param user_rate: User rate from shikimori
        :param anime_info: info about anime from shikimori
        """
        try:
            msg = (
                f"{anime_info['russian']} | {anime_info['name']}\n"
                f"<b>Рейтинг</b>: {anime_info['score']}\n"
                f"<b>Ваша Оценка</b>: {user_rate['score']}\n"
                f"<b>Просмотрено</b>: {user_rate['episodes']}: {anime_info['episodes_aired']} \n"
                + hlink("Перейти к аниме", SHIKI_URL + anime_info["url"])
            )
            return msg
        except Exception as e:
            logging.error(f"Error occurred while create anime_info_rate message - {e}")

    async def anime_info_msg(self, anime_info: dict) -> str:
        """
        create a message for anime_info
        :param anime_info: info about anime from shikimori
        """
        try:
            msg = (
                f"{anime_info['russian']} | {anime_info['name']}\n"
                f"<b>Рейтинг</b>: {anime_info['score']}\n"
                f"<b>Статус</b>: {anime_info['status']}\n"
                f"<b>Эпизодов</b> : {anime_info['episodes_aired']}\n"
                + hlink("Перейти к аниме", SHIKI_URL + anime_info["url"])
            )
            return msg
        except Exception as e:
            logging.error(f"Error occurred while create anime_info_rate message - {e}")


message_work = Message()
