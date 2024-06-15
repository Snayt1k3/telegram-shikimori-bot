from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Мои Списки 📔"),
        KeyboardButton(text="Профиль 😊"),
        KeyboardButton(text="Поиск 🔍"),
        width=4,
    )
    builder.row(
        KeyboardButton(text="Мои Подписки ❤️"),
        KeyboardButton(text="Рекомендации(dev) 📈"),
        KeyboardButton(text="Торрент(dev) ↕️"),
        width=4,
    )
    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup
