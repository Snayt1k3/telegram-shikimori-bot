from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Мои Списки 📔"),
        KeyboardButton(text="Профиль 😊"),
        KeyboardButton(text="Поиск 🔍"),
    )
    builder.row(
        KeyboardButton(text="Мои Подписки ❤️"),
        KeyboardButton(text="Рекомендации(dev) 📈"),
        KeyboardButton(text="Торрент(dev) ↕️"),
    )

    return builder.as_markup()
