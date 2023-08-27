import json
import os

import orjson

from database.database import DataBase
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.Anilibria.notifications import send_notification
from Keyboard.inline import Admin_kb
from .states import NotifyState
from bot import anilibria_client


async def admin(message: types.Message):
    admin_id = os.getenv("ADMIN_TG_ID")
    if str(message.from_user.id) != str(admin_id):
        return

    await message.answer(
        "Добро пожаловать в меню админа ShikiAnime Бота!", reply_markup=Admin_kb()
    )


async def NotifySetText(msg: types.Message):
    await msg.answer("Пришли мне текст, твоего уведомления пользователям.")
    await NotifyState.text.set()


async def NotifyEnd(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(f"Вот текст твоего уведомления - {msg.text}")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin, commands=["admin"])
    dp.register_message_handler(NotifySetText, commands=["notify"])
    dp.register_message_handler(NotifyEnd, state=NotifyState.text)
