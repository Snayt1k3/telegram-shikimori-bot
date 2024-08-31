import logging

from aiogram import types, Router, F
from src.presentation.telegram.common import Message, ReturnToUserRatesList
from src.presentation.telegram.common.constants import MY_LISTS_CMD
from src.presentation.telegram.common.keyboards import (
    user_lists_keyboard,
    AllListsEntryCallback,
    list_pagination_keyboard,
    AllListsPaginationCallback,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="ShikimoriListsRouter")
logger = logging.getLogger(__name__)


@router.message(F.text.contains(MY_LISTS_CMD))
async def all_lists_entry(msg: types.Message, messages: Message) -> None:
    kb = user_lists_keyboard()
    await msg.answer(text=messages.all_lists_msg, reply_markup=kb)


@router.callback_query(AllListsEntryCallback.filter())
async def get_user_rates(
    call: types.CallbackQuery,
    callback_data: AllListsEntryCallback,
    ioc: InteractorFactory,
    messages: Message,
) -> None:
    try:
        async with ioc.shikimori_get_list() as usecase:
            res = await usecase(call.from_user.id, callback_data.type)

        kb = list_pagination_keyboard(res.objs, callback_data.type.value)

        await call.message.answer_photo(
            photo=types.FSInputFile(
                "src/presentation/telegram/assets/img/angel-wings-anime.jpg"
            ),
            caption=messages.list_info_msg(res.length, 0),
            reply_markup=kb,
        )
    except Exception as e:
        logger.error(f"Error when getting user rates - {e}")
        await call.message.answer(
            "Упс, произошла ошибка получения списка, попробуйте еще раз."
        )


@router.callback_query(AllListsPaginationCallback.filter())
async def lists_pagination(
    call: types.CallbackQuery,
    callback_data: AllListsPaginationCallback,
    ioc: InteractorFactory,
    messages: Message,
):
    try:
        async with ioc.shikimori_get_list() as usecase:
            res = await usecase(call.from_user.id, callback_data.type)

        kb = list_pagination_keyboard(
            res.objs, callback_data.type.value, callback_data.page
        )

        await call.message.edit_caption(
            caption=messages.list_info_msg(res.length, callback_data.page),
            reply_markup=kb,
        )
    except Exception as e:
        logger.error(f"Error when paginating on list - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при перемещение по списку, попробуйте еще раз."
        )


@router.callback_query(ReturnToUserRatesList.filter())
async def return_to_user_list(
    call: types.CallbackQuery,
    callback_data: ReturnToUserRatesList,
    ioc: InteractorFactory,
    messages: Message,
) -> None:
    try:
        async with ioc.shikimori_get_list() as usecase:
            res = await usecase(call.from_user.id, callback_data.type)

        kb = list_pagination_keyboard(
            res.objs, callback_data.type.value, callback_data.page
        )

        await call.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.FSInputFile(
                    "src/presentation/telegram/assets/img/angel-wings-anime.jpg"
                )
            )
        )

        await call.message.edit_caption(
            caption=messages.list_info_msg(res.length, callback_data.page),
            reply_markup=kb,
        )
    except Exception as e:
        logger.error(f"Error when returning to list - {e}")
        await call.message.answer(
            "Упс, произошла ошибка при возращению к списку, попробуйте еще раз."
        )
