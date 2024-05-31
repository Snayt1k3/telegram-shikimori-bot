from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Cancel(CallbackData, prefix="cancel"):
    pass


def cancel_kb() -> ReplyKeyboardMarkup:
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
