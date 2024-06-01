from aiogram import types


async def cancel(msg: types.CallbackQuery):
    await msg.message.delete()
