from aiogram import types
from aiogram.filters import Command

from src.presentation.telegram.handlers.general.router import general


@general.message(Command("menu"))
async def main_menu(msg: types.Message):
    pass
