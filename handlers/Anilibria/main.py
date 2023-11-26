from aiogram import Dispatcher

from handlers.Anilibria.handlers.handlers import register_anilibria_handlers as handlers
from handlers.Anilibria.handlers.callbacks import register_al_callbacks
from handlers.Anilibria.utils.states import register_states_anilibria


def register_anilibria_handlers(dp: Dispatcher):
    handlers(dp)
    register_al_callbacks(dp)
    register_states_anilibria(dp)
