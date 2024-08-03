from aiogram import Router, types

from src.presentation.telegram.common import (
    Message,
    edit_user_rate_keyboard,
)
from src.presentation.telegram.common.keyboards.shikimori import (
    UserRateEdit,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="ShikimoriUserRate")


@router.callback_query(UserRateEdit.filter())
async def get_user_rate(
    call: types.CallbackQuery, callback_data: UserRateEdit, ioc: InteractorFactory
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(id=callback_data.id)

    msg = Message.user_rate_info_msg(user_rate)
    kb = edit_user_rate_keyboard(
        id=callback_data.id,
        last_episode=user_rate.title.episodes_aired,
        page=callback_data.page,
        list_type=callback_data.type,
    )

    await call.message.edit_media(
        media=types.InputMediaPhoto(media=types.URLInputFile(user_rate.title.image_url))
    )
    await call.message.edit_caption(caption=msg, reply_markup=kb)
