from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Literal
from src.handlers.auth.kb import logout_button, login_button


class ProfileCallback(CallbackData, prefix="profile"):
    action: Literal["rates"]


def profile_keyboard(is_authorized: bool = True) -> types.InlineKeyboardMarkup:
    auth_btn = logout_button() if is_authorized else login_button()

    rates_btn = types.InlineKeyboardButton(
        text="📕 Списки 📒", callback_data=ProfileCallback(action="rates").pack()
    )

    builder = InlineKeyboardBuilder()
    builder.row(auth_btn, rates_btn)

    return builder.adjust(2).as_markup()
