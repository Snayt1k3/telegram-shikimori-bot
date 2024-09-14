from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.presentation.telegram.common.constants import FOLLOW_LIST_PAGINATION
from src.application.dto import FollowListDTO
from src.presentation.telegram.common.keyboards.cancel import cancel_btn


class UnFollow(CallbackData, prefix="UnFollow"):
    id: int


class Follow(CallbackData, prefix="Follow"):
    id: int


class FollowListPagination(CallbackData, prefix="FollowListPagination"):
    offset: int


class ReturnToFollowList(CallbackData, prefix="ReturnToFollowList"):
    offset: int


class FollowItem(CallbackData, prefix="FollowItem"):
    id: int
    offset: int


def follows_keyboard(ls: FollowListDTO, offset: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in ls.follows:
        builder.button(
            text=item.ru, callback_data=FollowItem(offset=offset, id=item.id).pack()
        )

    # pagination
    buttons = []
    if offset != 0:
        buttons.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=FollowListPagination(
                    offset=offset - FOLLOW_LIST_PAGINATION
                ).pack(),
            )
        )

    if offset + FOLLOW_LIST_PAGINATION < len(ls.follows):
        buttons.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=FollowListPagination(
                    offset=offset + FOLLOW_LIST_PAGINATION
                ).pack(),
            )
        )

    builder.row(*buttons)

    return builder.adjust(1).as_markup()


def follow_item_keyboard(id: int, offset: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="❤️ Подписаться ❤️", callback_data=Follow(id=id).pack())
    builder.button(text="💔 Отписаться 💔", callback_data=UnFollow(id=id).pack())

    builder.button(
        text="<< Вернуться", callback_data=ReturnToFollowList(offset=offset).pack()
    )
    builder.add(cancel_btn())
    return builder.adjust(2).as_markup()
