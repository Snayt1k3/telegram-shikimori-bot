from aiogram import types, Router

from src.presentation.telegram.common.keyboards import AnilibriaTitle
from src.presentation.telegram.interactor_factory import InteractorFactory
from src.presentation.telegram.common import anilibria_title_kb, Message

router = Router(name="anilibria_title")


@router.callback_query(AnilibriaTitle.filter())
async def anilibria_title_edit(
    call: types.CallbackQuery,
    callback_data: AnilibriaTitle,
    ioc: InteractorFactory,
    messages: Message,
) -> None:
    async with ioc.get_anilibria_title() as usecase:
        res = await usecase(callback_data.id)

    msg = messages.anilibria_title_msg(res)
    kb = anilibria_title_kb(callback_data.id)
    await call.message.reply_photo(photo=res.img, caption=msg, reply_markup=kb)
