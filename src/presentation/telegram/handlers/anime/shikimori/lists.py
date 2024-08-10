from aiogram import types, Router, F
from src.presentation.telegram.common import Message, ReturnToUserRatesList
from src.presentation.telegram.common.constants import MY_LISTS_CMD
from src.presentation.telegram.common.keyboards import (
    all_lists_keyboard,
    AllListsEntryCallback,
    user_list_keyboard,
    AllListsPaginationCallback,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="ShikimoriListsRouter")


@router.message(F.text.contains(MY_LISTS_CMD))
async def all_lists(msg: types.Message) -> None:
    kb = all_lists_keyboard()
    await msg.answer(text=Message.all_lists_msg(), reply_markup=kb)


@router.callback_query(AllListsEntryCallback.filter())
async def get_user_rates(
    call: types.CallbackQuery,
    callback_data: AllListsEntryCallback,
    ioc: InteractorFactory,
) -> None:
    async with ioc.shikimori_get_list() as usecase:
        res = await usecase(call.from_user.id, callback_data.type)

    kb = user_list_keyboard(res.objs, callback_data.type.value)

    await call.message.answer_photo(
        photo=types.FSInputFile(
            "src/presentation/telegram/assets/img/angel-wings-anime.jpg"
        ),
        caption=Message.list_info_msg(res.length, 0),
        reply_markup=kb,
    )


@router.callback_query(AllListsPaginationCallback.filter())
async def lists_pagination(
    call: types.CallbackQuery,
    callback_data: AllListsPaginationCallback,
    ioc: InteractorFactory,
):
    async with ioc.shikimori_get_list() as usecase:
        res = await usecase(call.from_user.id, callback_data.type)

    kb = user_list_keyboard(res.objs, callback_data.type.value, callback_data.page)

    await call.message.edit_caption(
        caption=Message.list_info_msg(res.length, callback_data.page),
        reply_markup=kb,
    )


@router.callback_query(ReturnToUserRatesList.filter())
async def return_to_user_list(
    call: types.CallbackQuery,
    callback_data: ReturnToUserRatesList,
    ioc: InteractorFactory,
) -> None:
    async with ioc.shikimori_get_list() as usecase:
        res = await usecase(call.from_user.id, callback_data.type)

    kb = user_list_keyboard(res.objs, callback_data.type.value, callback_data.page)

    await call.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.FSInputFile(
                "src/presentation/telegram/assets/img/angel-wings-anime.jpg"
            )
        )
    )

    await call.message.edit_caption(
        caption=Message.list_info_msg(res.length, callback_data.page),
        reply_markup=kb,
    )
