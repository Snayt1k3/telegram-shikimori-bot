from aiogram import types

from src.presentation.telegram.handlers.anime.router import anime_router


@anime_router.message()
async def get_user_list_from_shiki(msg: types.Message):
    pass


@anime_router.callback_query()
async def pagination():
    pass
