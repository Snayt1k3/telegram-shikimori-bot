from aiogram import types

from src.presentation.telegram.common.keyboards import main_menu


async def send_menu(msg: types.Message):
    await msg.reply(text="Ok", reply_markup=main_menu())

