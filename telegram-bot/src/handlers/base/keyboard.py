from aiogram import types


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
