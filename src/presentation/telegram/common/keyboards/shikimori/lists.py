from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.dto import UserRateDTO
from src.application.enums import ShikimoriListType
from src.presentation.telegram.common.constants import USER_LIST_PAGINATION


class AllListsCallback(CallbackData, prefix="all_lists"):
    type: ShikimoriListType


class AllListsPaginationCallback(CallbackData, prefix="all_lists_pagination_callback"):
    type: ShikimoriListType
    page: int = 0


class UserRateEdit(CallbackData, prefix="user_rate_edit"):
    id: int
    page: int
    type: ShikimoriListType


def all_lists_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Запланированное",
        callback_data=AllListsCallback(type=ShikimoriListType.PLANNED).pack(),
    )
    builder.button(
        text="Брошенное",
        callback_data=AllListsCallback(type=ShikimoriListType.DROPPED).pack(),
    )
    builder.button(
        text="Пересматриваю",
        callback_data=AllListsCallback(type=ShikimoriListType.REWATCHING).pack(),
    )
    builder.button(
        text="Смотрю",
        callback_data=AllListsCallback(type=ShikimoriListType.WATCHING).pack(),
    )
    builder.button(
        text="Просмотренное",
        callback_data=AllListsCallback(type=ShikimoriListType.COMPLETED).pack(),
    )
    builder.button(
        text="Отложено",
        callback_data=AllListsCallback(type=ShikimoriListType.ON_HOLD).pack(),
    )
    return builder.adjust(1, 2).as_markup()


def user_list_keyboard(
    titles: list[UserRateDTO], listType: ShikimoriListType, page: int = 0
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for title in titles[page : page + USER_LIST_PAGINATION]:
        builder.row(
            InlineKeyboardButton(
                text=title.title.title_ru,
                callback_data=UserRateEdit(
                    id=title.id, type=listType, page=page
                ).pack(),
            )
        )

    buttons = []

    if 0 < page + USER_LIST_PAGINATION:
        buttons.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=AllListsPaginationCallback(
                    page=page - USER_LIST_PAGINATION, type=listType
                ).pack(),
            ),
        )

    if page < len(titles):
        buttons.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=AllListsPaginationCallback(
                    page=page + USER_LIST_PAGINATION, type=listType
                ).pack(),
            ),
        )

    builder.row(*buttons)

    return builder.as_markup()
