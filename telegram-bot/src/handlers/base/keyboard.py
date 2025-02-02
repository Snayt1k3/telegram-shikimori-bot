from aiogram import types
from aiogram.filters.callback_data import CallbackData


class CancelCallback(CallbackData, prefix="cancel"):
    pass


def start_keyboard() -> types.ReplyKeyboardMarkup:
    btns = [
        [
            types.KeyboardButton(text="👤 Профиль"),
            types.KeyboardButton(text="🔍 Поиск"),
        ],
        [
            types.KeyboardButton(text="Статистика"),
            types.KeyboardButton(text="Рекомендации"),
        ],
    ]
    return types.ReplyKeyboardMarkup(keyboard=btns)


def cancel_button() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text="❌ Удалить", callback_data=CancelCallback().pack()
    )
