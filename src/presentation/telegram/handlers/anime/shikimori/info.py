from aiogram import Router, types

from src.presentation.telegram.common.keyboards.shikimori import (
    UserRateEdit,
    EpisodePaginationCallback,
    EpisodeEditCallback,
    ReturnEditTitleCallback,
    MarkStatusTitleCallback,
)
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="shikimori_info")


@router.callback_query(UserRateEdit.filter())
async def get_info_about_anime(
    call: types.CallbackQuery, callback_data: UserRateEdit, ioc: InteractorFactory
) -> None:
    pass


@router.callback_query(ReturnEditTitleCallback.filter())
async def return_to_edit_title(
    call: types.CallbackQuery,
    callback_data: ReturnEditTitleCallback,
    ioc: InteractorFactory,
) -> None:
    pass


@router.callback_query(EpisodeEditCallback.filter())
async def mark_episode(
    call: types.CallbackQuery,
    callback_data: EpisodeEditCallback,
    ioc: InteractorFactory,
) -> None:
    pass


@router.callback_query(EpisodePaginationCallback.filter())
async def episode_pagination(
    call: types.CallbackQuery,
    callback_data: EpisodePaginationCallback,
    ioc: InteractorFactory,
) -> None:
    pass


@router.callback_query(MarkStatusTitleCallback.filter())
async def mark_status_title(
    call: types.CallbackQuery,
    callback_data: MarkStatusTitleCallback,
    ioc: InteractorFactory,
) -> None:
    pass
