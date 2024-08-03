from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton


class Cancel(CallbackData, prefix="cancel"):
    pass


def cancel_btn() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="Отмена ❌", callback_data=Cancel().pack())
