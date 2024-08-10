from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.dto.title import SearchResultsDTO
from src.application.enums import SearchEngineEnum
from .shikimori import ShikimoriViewTitle
from .anilibria import AnilibriaTitle
from .. import constants


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

    for obj in res.results[: constants.MAX_SEARCH_RESPONSE_SIZE]:
        builder.button(
            text=obj.ru,
            callback_data=AnilibriaTitle(id=obj.id).pack(),
        )

    return builder.adjust(1).as_markup()


def shikimori_response_kb(res: SearchResultsDTO) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for obj in res.results[: constants.MAX_SEARCH_RESPONSE_SIZE]:
        builder.button(text=obj.ru, callback_data=ShikimoriViewTitle(id=obj.id).pack())

    return builder.adjust(1).as_markup()
