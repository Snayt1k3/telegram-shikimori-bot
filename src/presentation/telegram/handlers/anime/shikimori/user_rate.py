import logging

from aiogram import Router, types

from src.presentation.telegram.common import (
    Message,
    edit_user_rate_anime_keyboard,
    edit_user_rate_manga_keyboard,
    ShikimoriDeleteUserRate,
)
from src.presentation.telegram.common.keyboards.shikimori import (
    UserRateEdit,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="ShikimoriUserRateRouter")
logger = logging.getLogger(__name__)


@router.callback_query(UserRateEdit.filter())
async def get_user_rate(
    call: types.CallbackQuery, callback_data: UserRateEdit, ioc: InteractorFactory
) -> None:
    try:
        async with ioc.get_user_rate() as usecase:
            user_rate = await usecase(id=callback_data.id)

        if user_rate.target_type == "Anime":
            msg = Message.user_rate_anime_msg(user_rate)
            kb = edit_user_rate_anime_keyboard(
                id=callback_data.id,
                last_episode=user_rate.title.episodes_aired,
                page=callback_data.page,
                list_type=callback_data.type,
            )
        else:
            msg = Message.user_rate_manga_msg(user_rate)
            kb = edit_user_rate_manga_keyboard(
                id=callback_data.id,
                page=callback_data.page,
                list_type=callback_data.type,
            )

        await call.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.URLInputFile(user_rate.title.image_url)
            )
        )
        await call.message.edit_caption(caption=msg, reply_markup=kb)
    except Exception as e:
        logger.error(f"Error when getting information about user rate - {e}")
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriDeleteUserRate.filter())
async def delete_user_rate(
    call: types.CallbackQuery,
    callback_data: ShikimoriDeleteUserRate,
    ioc: InteractorFactory,
) -> None:
    try:
        async with ioc.delete_user_rate() as usecase:
            await usecase(callback_data.id)

        await call.message.answer("Удаление прошло успешно")

    except Exception as e:
        logger.error(f"Error when deleting a user - {e}")
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")
