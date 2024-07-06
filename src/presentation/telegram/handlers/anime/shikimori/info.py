from aiogram import Router, types

from src.application.dto import UserRateUpdateDTO
from src.presentation.telegram.common import (
    Message,
    edit_title_keyboard,
    episode_keyboard,
)
from src.presentation.telegram.common.keyboards.shikimori import (
    UserRateEdit,
    ShikimoriEpisodePagination,
    ShikimoriUpdateEpisode,
    ShikimoriEditStatus,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_info")


@router.callback_query(UserRateEdit.filter())
async def get_info_about_anime(
    call: types.CallbackQuery, callback_data: UserRateEdit, ioc: InteractorFactory
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(call.from_user.id, callback_data.id)

    msg = Message.user_rate_info_msg(user_rate)
    kb = edit_title_keyboard(
        id=callback_data.id,
        last_episode=user_rate.title.episodes_aired,
    )

    await call.message.reply_photo(
        photo=user_rate.title.image_url, caption=msg, reply_markup=kb
    )


@router.callback_query(ShikimoriUpdateEpisode.filter())
async def mark_episode(
    call: types.CallbackQuery,
    callback_data: ShikimoriUpdateEpisode,
    ioc: InteractorFactory,
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(id_telegram=call.from_user.id, id=callback_data.id)

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


@router.callback_query(ShikimoriEditStatus.filter())
async def mark_status_title(
    call: types.CallbackQuery,
    callback_data: ShikimoriEditStatus,
    ioc: InteractorFactory,
) -> None:
    async with ioc.get_user_rate() as usecase:
        user_rate = await usecase(id_telegram=call.from_user.id, id=callback_data.id)

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
