from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Cancel(CallbackData, prefix="cancel"):
    pass

def cancel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Отмена", callback_data=CallbackData().pack())

    return builder.as_markup()
