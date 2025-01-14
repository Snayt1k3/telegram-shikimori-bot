from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Literal


class AuthCallBack(CallbackData, prefix="auth"):
    action: Literal["sign", "logout"]


class ProfileCallback(CallbackData, prefix="profile"):
    action: Literal["rates"]


def profile_keyboard(is_authorized: bool = True) -> types.InlineKeyboardMarkup:
    auth_btn = types.InlineKeyboardButton(
        text="❌ Деавторизоваться ❌",
        callback_data=AuthCallBack(action="logout").pack(),
    )

    if is_authorized:
        auth_btn = types.InlineKeyboardButton(
            text="✅ Авторизоваться ✅",
            callback_data=AuthCallBack(action="sign").pack(),
        )

    rates_btn = types.InlineKeyboardButton(
        text="📕 Списки 📒", callback_data=ProfileCallback(action="rates").pack()
    )

    builder = InlineKeyboardBuilder()
    builder.row(auth_btn, rates_btn)

    return builder.adjust(2).as_markup()
