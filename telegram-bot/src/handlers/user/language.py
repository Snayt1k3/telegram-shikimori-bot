from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext

from src.handlers.keyboard import user

language_router = Router(name="language")


@language_router.message(Command("lang"))
async def lang_message(message: types.Message, i18n: I18nContext):
    text = i18n.get("choose-lang-message")
    await message.answer(text, reply_markup=user.language_kb())


@language_router.callback_query(user.LanguageCallback.filter())
async def lang_callback_query(clk: types.CallbackQuery, callback_data: user.LanguageCallback, i18n: I18nContext):
    text = i18n.get("picked-lang-message", locale=callback_data.lang_code)
    # TODO: Добавить Логику
    await clk.answer()
    await clk.message.answer(text)
