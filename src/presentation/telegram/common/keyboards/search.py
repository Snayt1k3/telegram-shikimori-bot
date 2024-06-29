from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.adapters.enums import SearchEngineEnum
from src.application.dto.title import SearchResultsDTO
from src.presentation.telegram.common import AnilibriaTitle, ShikimoriTitle


class SearchCallback(CallbackData, prefix="Search"):
    engine: SearchEngineEnum


def search_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Шикимори",
        callback_data=SearchCallback(engine=SearchEngineEnum.shikimori).pack(),
    )
    builder.button(
        text="Анилибрия",
        callback_data=SearchCallback(engine=SearchEngineEnum.anilibria).pack(),
    )

    return builder.as_markup()


def anilibria_response_kb(res: SearchResultsDTO) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for obj in res.results:
        builder.button(text=obj.ru, callback_data=AnilibriaTitle(id=obj.id).pack())

    return builder.as_markup()


def shikimori_response_kb(res: SearchResultsDTO) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for obj in res.results:
        builder.button(text=obj.ru, callback_data=ShikimoriTitle(id=obj.id).pack())

    return builder.as_markup()
