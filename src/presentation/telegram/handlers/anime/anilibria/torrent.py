from aiogram import types

from src.presentation.telegram.handlers.anime.router import anime_router


@anime_router.callback_query()
async def torrent(call: types.CallbackQuery):
    pass
