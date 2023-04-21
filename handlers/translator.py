from aiogram import types
from googletrans import Translator

from database.database import DataBase


async def get_user_code_lang(chat_id) -> str:
    db = DataBase()
    res = db.find_one('chat_id', chat_id, 'lang_users')

    return res['lang_code'] if res else 'en'


async def set_lang_code(message: types.Message):
    db = DataBase()
    record = db.find_one('chat_id', message.chat.id, 'lang_users')

    if record:
        db.update_one('lang_users', 'chat_id', message.chat.id, {'lang_code': message.from_user.language_code})

    else:
        db.insert_into_collection('lang_users', {'chat_id': message.chat.id,
                                                 'lang_code': message.from_user.language_code})


async def translate_text(message: types.Message, s: str):
    code = await get_user_code_lang(message.chat.id)
    translator = Translator()
    translated_text = translator.translate(s, dest=code).text
    return translated_text
