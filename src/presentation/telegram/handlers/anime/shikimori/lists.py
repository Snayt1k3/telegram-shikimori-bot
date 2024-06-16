from aiogram import types, Router, F
from aiogram.filters import Command

from src.presentation.telegram.common import Message
from src.presentation.telegram.common.keyboards import (
    all_lists_keyboard,
    AllListsCallback,
    user_list_keyboard,
    AllListsPaginationCallback
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_lists")


@router.message(F.text.lower() == "списки", Command("lists"))
async def all_lists(msg: types.Message) -> None:
    kb = all_lists_keyboard()
    await msg.answer(text=Message.all_lists_msg(), reply_markup=kb)


@router.callback_query(AllListsCallback.filter())
async def get_user_list_from_shiki(
    call: types.CallbackQuery, callback_data: AllListsCallback, ioc: InteractorFactory
) -> None:
    async with ioc.shikimori_get_list() as usecase:
        res = await usecase(call.from_user.id, callback_data.type)

    kb = user_list_keyboard(res.objs, callback_data.type.value)

    await call.message.answer_photo(
        photo=types.InputFile("src/presentation/telegram/assets/img/angel-wings-anime.jpg"),
        caption=Message.list_info_msg(res.length, 0),
        reply_markup=kb,
    )


@router.callback_query(AllListsPaginationCallback.filter())
async def pagination(call: types.CallbackQuery, callback_data: AllListsPaginationCallback, ioc: InteractorFactory):
    async with ioc.shikimori_get_list() as usecase:
        res = await usecase(call.from_user.id, callback_data.type)

    kb = user_list_keyboard(res.objs, callback_data.type.value, callback_data.page)

    await call.message.edit_caption(
        caption=Message.list_info_msg(res.length, callback_data.page),
        reply_markup=kb,
    )
