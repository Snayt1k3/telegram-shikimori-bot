from aiogram import types
from Keyboard.shikimori.inline import keyboard_user_rate_view
from database.repositories.shikimori import shiki_repository
from handlers.Shikimori.utils.shiki_api import shiki_api
from database.dto.animes import ShikimoriAnime


async def message_user_list(message: types.Message, collection: str) -> None:
    """
    send message with info about user list
    :param message: message
    :param collection: MongoDB collection
    """
    animes = await shiki_repository.get_one(collection, {"chat_id": message.chat.id})
    kb = await keyboard_user_rate_view(
        animes["animes"],
        collection,
    )
    await message.reply_photo(
        open("misc/img/pic1.png", "rb"),
        "Выберите интересующее вас аниме.",
        reply_markup=kb,
    )
