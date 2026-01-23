from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class LanguageCallback(CallbackData, prefix="LanguageCallback"):
    lang_code: Literal["ru", "en"]


def language_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🇷🇺 Русский", callback_data=LanguageCallback(lang_code="ru").pack())
    kb.button(text="🇬🇧 English", callback_data=LanguageCallback(lang_code="en").pack())

    return kb.as_markup()
