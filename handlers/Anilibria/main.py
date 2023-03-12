from aiogram import Dispatcher, types
from .anime_functions import search_on_anilibria
from handlers.Anilibria.anilibria_handlers import register_anilibria_handlers as handlers


def register_anilibria_handlers(dp: Dispatcher):
    handlers(dp)

