from aiogram import types

from src.presentation.telegram.handlers.general.router import general


@general.message()
async def about(msg: types.Message):
    pass
