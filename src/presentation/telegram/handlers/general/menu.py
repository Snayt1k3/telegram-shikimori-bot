from aiogram import types
from aiogram.filters import Command

from src.presentation.telegram.handlers.general.router import general
from src.presentation.telegram.common.keyboards import main_menu

@general.message(Command("menu"))
async def menu(msg: types.Message):
    await msg.reply(text="Ok", reply_markup=main_menu())

