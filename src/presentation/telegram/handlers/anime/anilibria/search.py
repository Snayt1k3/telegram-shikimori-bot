from aiogram import types

from src.presentation.telegram.handlers.anime.router import anime_router


@anime_router.message()
async def start_search(msg: types.Message):
    pass


@anime_router.message()  # todo создать состояние
async def search_on_anilibria():
    pass
