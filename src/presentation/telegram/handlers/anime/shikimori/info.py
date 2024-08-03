from aiogram import Router, types

from src.presentation.telegram.common import (
    Message,
    edit_title_keyboard,
)
from src.presentation.telegram.common.keyboards.shikimori import (
    ShikimoriViewTitle,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_info")


@router.callback_query(ShikimoriViewTitle.filter())
async def get_anime_info(
    call: types.CallbackQuery,
    callback_data: ShikimoriViewTitle,
    ioc: InteractorFactory,
) -> None:

    async with ioc.get_shikimori_title() as usecase:
        res = await usecase(callback_data.id)

    text = Message.shikimori_title_msg(res)
    kb = edit_title_keyboard(res.id, res.episodes_aired)

    await call.message.reply_photo(
        caption=text, reply_markup=kb, photo=types.URLInputFile(res.image_url)
    )
