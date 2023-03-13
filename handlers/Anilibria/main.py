from aiogram import Dispatcher

from handlers.Anilibria.anilibria_handlers import register_anilibria_handlers as handlers
from handlers.Anilibria.callbacks import register_al_callbacks


def register_anilibria_handlers(dp: Dispatcher):
    handlers(dp)
    register_al_callbacks(dp)
