from aiogram import types
from googletrans import Translator

from bot import db_client


async def get_user_code_lang(chat_id) -> str:
    # DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["lang_users"]
    res = collection.find_one({'chat_id': chat_id})
    return res['lang_code'] if res else 'en'


async def set_lang_code(message: types.Message):
    # DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["lang_users"]

    record = collection.find_one({'chat_id': message.chat.id})
    if record:
        collection.update_one({'chat_id': message.chat.id}, {'$set': {'lang_code': message.from_user.language_code}})

    else:
        collection.insert_one({'chat_id': message.chat.id,
                               'lang_code': message.from_user.language_code})


async def translate_text(message: types.Message, s: str):
    code = await get_user_code_lang(message.chat.id)
    translator = Translator()
    # Get message and translate
    translated_text = translator.translate(s, dest=code).text
    return translated_text
