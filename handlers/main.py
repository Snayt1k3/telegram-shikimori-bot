from aiogram import Dispatcher
from handlers.Shikimori.main import register_shiki_handlers
from handlers.Anilibria.main import register_anilibria_handlers


def register_handlers(dp: Dispatcher):
    register_shiki_handlers(dp)
    register_anilibria_handlers(dp)
