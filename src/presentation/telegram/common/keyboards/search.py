from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.application.dto.title import SearchResultsDTO
from src.adapters.enums import SearchEngineEnum
from src.presentation.telegram.common.keyboards.shikimori import UserRateEdit


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
        builder.button(text=obj.ru)  # todo добавить clk для Anime

    return builder.as_markup()


def shikimori_response_kb(res: SearchResultsDTO) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for obj in res.results:
        builder.button(text=obj.ru)  # todo добавить clk для Anime

    return builder.as_markup()
