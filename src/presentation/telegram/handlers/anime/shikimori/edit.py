from dataclasses import asdict

from aiogram import types, Router

from src.application.dto import UserRateUpdateDTO
from src.presentation.telegram.common import (
    ShikimoriUpdateStatus,
    ShikimoriEpisodePagination,
    ShikimoriUpdateEpisode,
    ShikimoriDeleteUserRate,
    episode_keyboard,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_edit")


@router.callback_query(ShikimoriUpdateEpisode.filter())
async def update_episode(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateEpisode,
    ioc: InteractorFactory,
):
    try:

        async with ioc.get_user_rate() as usecase:
            user_rate = usecase(id=callback_data.id)

        update_obj = UserRateUpdateDTO.from_dict(asdict(user_rate))
        update_obj.episodes = callback_data.episode

        async with ioc.get_credentials() as usecase:
            creds = await usecase(call.from_user.id)

        async with ioc.update_user_rate() as usecase:
            await usecase(update_obj, creds.access)

        await call.message.answer("Обновление прошло успешно!")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriUpdateStatus.filter())
async def update_title_status(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateStatus,
    ioc: InteractorFactory,
):
    try:

        async with ioc.get_user_rate() as usecase:
            user_rate = usecase(id=callback_data.id)

        update_obj = UserRateUpdateDTO.from_dict(asdict(user_rate))
        update_obj.status = callback_data.status.value

        async with ioc.get_credentials() as usecase:
            creds = await usecase(call.from_user.id)

        async with ioc.update_user_rate() as usecase:
            await usecase(update_obj, creds.access)

        await call.message.answer("Обновление прошло успешно!")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriDeleteUserRate.filter())
async def delete_user_rate(
    call: types.CallbackQuery,
    callback_data: ShikimoriDeleteUserRate,
    ioc: InteractorFactory,
):
    try:
        async with ioc.delete_user_rate() as usecase:
            await usecase(callback_data.id)

        await call.message.answer("Удаление прошло успешно")

    except Exception as e:
        await call.message.answer("Упс, Что-то пошло не так, попробуйте еще раз.")


@router.callback_query(ShikimoriUpdateStatus.filter())
async def update_user_rate_status(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateStatus,
    ioc: InteractorFactory,
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(id=callback_data.id)

    obj = UserRateUpdateDTO(
        id=callback_data.id,
        episodes=user_rate.episodes,
        status=str(callback_data.status),
        score=user_rate.score,
        volumes=user_rate.volumes,
        chapters=user_rate.chapters,
        rewatches=user_rate.rewatches,
    )

    async with ioc.get_credentials() as usecase:
        creds = await usecase(call.from_user.id)

    async with ioc.update_user_rate() as usecase:
        await usecase(obj, creds.access)

    await call.message.reply("Обновление Прошло успешно")
