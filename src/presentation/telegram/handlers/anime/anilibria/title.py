from aiogram import types, Router

from src.presentation.telegram.common.keyboards import AnilibriaTitle
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="anilibria_title")


@router.callback_query(AnilibriaTitle.filter())
async def anilibria_title_edit(
    call: types.CallbackQuery, ioc: InteractorFactory
) -> None:
    pass
