from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.enums import ShikimoriListType


class AnilibriaTitle(CallbackData, prefix="anilibria_title"):
    id: int


def anilibria_title() -> types.InlineKeyboardMarkup:
    """
    Keyboard for action with anime from anilibria.api

    Available actions:
    - follow/unfollow
    - torrent
    - search on shikimori by name
    """
    pass  # todo подумать на кнопками
