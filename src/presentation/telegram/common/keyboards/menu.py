from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.presentation.telegram.common.constants import (
    MY_LISTS_CMD,
    SEARCH_CMD,
    TORRENT_CMD,
)


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MY_LISTS_CMD),
        KeyboardButton(text="Профиль 😊"),
        KeyboardButton(text=SEARCH_CMD),
        width=4,
    )
    builder.row(
        KeyboardButton(text="Мои Подписки ❤️"),
        KeyboardButton(text="Рекомендации(dev) 📈"),
        KeyboardButton(text=TORRENT_CMD),
        width=4,
    )
    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup
