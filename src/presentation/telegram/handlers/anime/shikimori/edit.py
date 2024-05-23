from aiogram import types

from src.presentation.telegram.handlers.anime.router import anime_router


@anime_router.callback_query()
async def edit_episode(call: types.CallbackQuery):
    pass


@anime_router.callback_query()
async def pagination_episode(call: types.CallbackQuery):
    pass


@anime_router.callback_query()
async def edit_status(call: types.CallbackQuery):
    pass


@anime_router.callback_query()
async def delete_title(call: types.CallbackQuery):
    pass
