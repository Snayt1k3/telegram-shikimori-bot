from typing import Literal

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AuthCallBack(CallbackData, prefix="auth"):
    action: Literal["login", "logout"]


class LogoutCallback(CallbackData, prefix="logout"):
    action: Literal["Yes", "No"]


def logout_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(
            text="✅ Уверен", callback_data=LogoutCallback(action="Yes").pack()
        ),
        types.InlineKeyboardButton(
            text="❌ Не уверен", callback_data=LogoutCallback(action="No").pack()
        ),
    )
    return kb.as_markup()


def login_button() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text="✅ Авторизоваться ✅",
        callback_data=AuthCallBack(action="login").pack(),
    )


def logout_button() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(
        text="❌ Деавторизоваться ❌",
        callback_data=AuthCallBack(action="logout").pack(),
    )
