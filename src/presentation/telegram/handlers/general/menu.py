from aiogram import types

from src.presentation.telegram.handlers.general.router import general


@general.message()
async def main_menu(msg: types.Message):
    pass
