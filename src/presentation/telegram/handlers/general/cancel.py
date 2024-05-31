from aiogram import types

from src.presentation.telegram.common.keyboards import Cancel
from src.presentation.telegram.handlers.general.router import general


@general.callback_query(Cancel.filter())
async def cancel(msg: types.CallbackQuery):
    await msg.message.delete()
