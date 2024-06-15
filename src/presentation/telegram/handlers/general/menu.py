from aiogram import types, Router
from aiogram.filters import Command

from src.presentation.telegram.common.keyboards import main_menu

router = Router(name="menu")


@router.message(Command("menu"))
async def send_menu(msg: types.Message):
    await msg.reply(text="Ok", reply_markup=main_menu())

