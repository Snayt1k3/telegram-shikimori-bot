from aiogram import types

from src.presentation.telegram.handlers.general.router import general


@general.callback_query()
async def cancel(msg: types.CallbackQuery):
    pass
