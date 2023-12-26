from aiogram import Dispatcher
from handlers.Shikimori.handlers.handlers import register_handlers
from handlers.Shikimori.handlers.callbacks import register_callbacks


def register_shiki_handlers(dp: Dispatcher):
    register_handlers(dp)
    register_callbacks(dp)
