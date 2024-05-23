from aiogram import types

from src.presentation.telegram.handlers.notification.router import notify


@notify.callback_query()
async def follow(call: types.CallbackQuery):
    pass


@notify.callback_query()
async def unfollow(call: types.CallbackQuery):
    pass


@notify.callback_query()
async def user_follows(call: types.CallbackQuery):
    pass
