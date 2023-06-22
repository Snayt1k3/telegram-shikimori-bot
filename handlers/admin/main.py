from aiogram import Dispatcher

from handlers.admin.handlers import register_handlers
from handlers.admin.callbacks import register_callbacks


def register_admin_handlers(dp: Dispatcher):
    register_handlers(dp)
    register_callbacks(dp)