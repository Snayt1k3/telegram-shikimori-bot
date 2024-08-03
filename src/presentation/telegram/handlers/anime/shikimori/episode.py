from aiogram import Router, types

from src.application.dto import UserRateUpdateDTO
from src.presentation.telegram.common import (
    episode_keyboard,
)
from src.presentation.telegram.common.keyboards.shikimori import (
    ShikimoriEpisodePagination,
    ShikimoriEpisodePaginationStart,
    ShikimoriUpdateEpisode,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="ShikimoriEpisodeRouter")


@router.callback_query(ShikimoriEpisodePagination.filter())
async def episode_pagination(
    call: types.CallbackQuery,
    callback_data: ShikimoriEpisodePagination,
) -> None:

    kb = episode_keyboard(
        id=callback_data.id,
        page=callback_data.page,
        last_episode=callback_data.last_episode,
    )

    await call.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(ShikimoriEpisodePaginationStart.filter())
async def episode_pagination(
    call: types.CallbackQuery,
    callback_data: ShikimoriEpisodePaginationStart,
) -> None:

    kb = episode_keyboard(
        id=callback_data.id,
        page=callback_data.page,
        last_episode=callback_data.last_episode,
    )

    await call.message.answer(reply_markup=kb, text="Выберите эпизод:")


@router.callback_query(ShikimoriUpdateEpisode.filter())
async def mark_episode(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateEpisode,
    ioc: InteractorFactory,
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(id=callback_data.id)

    obj = UserRateUpdateDTO(
        id=callback_data.id,
        episodes=callback_data.episode,
        status=user_rate.status,
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
