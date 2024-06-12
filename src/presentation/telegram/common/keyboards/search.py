from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.adapters.enums import SearchEngineEnum


class SearchCallback(CallbackData, prefix="Search"):
    engine: SearchEngineEnum

def search_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Шикимори", callback_data=SearchCallback(engine=SearchEngineEnum.shikimori).pack())
    builder.button(text="Анилибрия", callback_data=SearchCallback(engine=SearchEngineEnum.anilibria).pack())

    return builder.as_markup()
