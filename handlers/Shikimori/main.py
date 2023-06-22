from aiogram import Dispatcher
from .handlers import register_handlers
from .callbacks import register_callbacks


def register_shiki_handlers(dp: Dispatcher):
    register_handlers(dp)
    register_callbacks(dp)
