from dataclasses import asdict

from aiogram import types, Router

from src.application.dto import UserRateUpdateDTO
from src.presentation.telegram.common import (
    ShikimoriEditStatus,
    ShikimoriEpisodePagination,
    ShikimoriUpdateEpisode,
    ShikimoriDeleteTitle,
    episode_keyboard,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_edit")


@router.callback_query(ShikimoriUpdateEpisode.filter())
async def edit_episode(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateEpisode,
    ioc: InteractorFactory,
):
    try:

        async with ioc.get_user_rate() as usecase:
            user_rate = usecase(call.from_user.id, callback_data.id)

        update_obj = UserRateUpdateDTO.from_dict(asdict(user_rate))
        update_obj.episodes = callback_data.episode

        async with ioc.get_credentials() as usecase:
            creds = await usecase(call.from_user.id)

        async with ioc.update_user_rate() as usecase:
            await usecase(update_obj, creds.access)

        await call.message.answer("Обновление прошло успешно!")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriEpisodePagination.filter())
async def pagination_episode(
    call: types.CallbackQuery,
    callback_data: ShikimoriEpisodePagination,
):
    kb = episode_keyboard(callback_data.id, callback_data.page, callback_data.page)
    await call.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(ShikimoriEditStatus.filter())
async def edit_status(
    call: types.CallbackQuery,
    callback_data: ShikimoriEditStatus,
    ioc: InteractorFactory,
):
    try:

        async with ioc.get_user_rate() as usecase:
            user_rate = usecase(call.from_user.id, callback_data.id)

        update_obj = UserRateUpdateDTO.from_dict(asdict(user_rate))
        update_obj.status = callback_data.status.value

        async with ioc.get_credentials() as usecase:
            creds = await usecase(call.from_user.id)

        async with ioc.update_user_rate() as usecase:
            await usecase(update_obj, creds.access)

        await call.message.answer("Обновление прошло успешно!")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriDeleteTitle.filter())
async def delete_title(
    call: types.CallbackQuery,
    callback_data: ShikimoriDeleteTitle,
    ioc: InteractorFactory,
):
    try:
        async with ioc.delete_user_rate() as usecase:
            await usecase(callback_data.id)

        await call.message.answer("Удаление прошло успешно")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")
