from aiogram import Dispatcher, types

from .anime_functions import search_on_anilibria


async def test(message: types.Message):
    await search_on_anilibria('Мастера Меча онлайн 2')


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(test, commands=['test'])
