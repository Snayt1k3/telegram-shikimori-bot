from aiogram import Dispatcher
from .shikimori_anime import register_anime_handlers
from .shikimori_profile import register_profile_handlers
from .callbacks import register_callbacks


def register_shiki_handlers(dp: Dispatcher):
    register_anime_handlers(dp)
    register_profile_handlers(dp)
    register_callbacks(dp)
