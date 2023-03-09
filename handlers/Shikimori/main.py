from aiogram import Dispatcher
from .shikimori_anime_handlers import register_anime_handlers
from .shikimori_handlers import register_profile_handlers


def register_shiki_handlers(dp: Dispatcher):
    register_anime_handlers(dp)
    register_profile_handlers(dp)
