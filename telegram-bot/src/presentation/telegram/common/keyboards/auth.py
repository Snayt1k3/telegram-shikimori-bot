from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SignOut(CallbackData, prefix="signout"):
    delete: bool = False


def signout_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🚪 Разлогиниться",
        callback_data=SignOut(delete=True).pack(),
    )
    builder.button(
        text="❌ Отменить",
        callback_data=SignOut(delete=False).pack(),
    )

    return builder.as_markup()
