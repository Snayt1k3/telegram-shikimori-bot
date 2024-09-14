from aiogram import types, Router

from src.presentation.telegram.common import Cancel

router = Router(name="cancel")

@router.callback_query(Cancel.filter())
async def cancel(msg: types.CallbackQuery):
    await msg.message.delete()
