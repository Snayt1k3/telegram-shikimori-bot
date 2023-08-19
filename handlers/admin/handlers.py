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


async def update_db_to_new(message: types.Message):
    all_follows = await DataBase.find("user_follows")
    async for user_follow in all_follows:
        animes = [
            await anilibria_client.get_title(i) for i in user_follow.get("animes")
        ]

        await DataBase.update_one(
            "user_follows",
            "chat_id",
            message.chat.id,
            {
                "chat_id": message.chat.id,
                "animes": [
                    {
                        "title_en": title.names.en,
                        "title_ru": title.names.ru,
                        "id": title.id,
                    }
                    for title in animes
                ],
            },
        )


async def NotifySetText(msg: types.Message):
    await msg.answer("Пришли мне текст, твоего уведомления пользователям.")
    await NotifyState.text.set()


async def NotifyEnd(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(f"Вот текст твоего уведомления - {msg.text}")


async def test(msg: types.Message):
    with open("test.json", "r", encoding="UTF-8") as file:
        file = json.load(file)
    await send_notification(file)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin, commands=["admin"])
    dp.register_message_handler(test, commands=["test"])
    dp.register_message_handler(NotifySetText, commands=["notify"])
    dp.register_message_handler(update_db_to_new, commands=["update_db"])
    dp.register_message_handler(NotifyEnd, state=NotifyState.text)
