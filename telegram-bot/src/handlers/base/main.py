from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from keyboard import start_keyboard

router = Router(name="BaseCommands")


@router.message(CommandStart())
async def start_handler(m: types.Message) -> None:
    await m.reply(
        """Хочешь, чтобы бот заработал на полную? Тогда не ленись и вызови <b>👤 Профиль</b>, партнер~ 😜""",
        reply_markup=start_keyboard(),
    )


@router.message(Command("cancel"))
async def cancel_state(m: types.Message, state: FSMContext) -> None:
    await m.answer(
        "Окей, процесс остановлен. Если захочешь попробовать снова, просто сообщи мне. 😊"
    )
    await state.clear()


@router.message(Command("help"))
async def help_handler(m: types.Message) -> None:
    await m.reply_photo(
        caption="""
    Эй, партнёр, кажется, тебе нужна помощь? 😏
    Вот что я умею для тебя:
    Управление списками на Shikimori: Добавляй, удаляй или обновляй, как хочешь, я всё сделаю!
    Статистика: Покажу твою активность за год — и по мне, и по Shikimori~
    Рекомендации с помощью AI: Хочешь что-то посмотреть или почитать? Я знаю, что тебе понравится! 😘
    Команды:
    /start — Начнём наше путешествие вместе~
    /profile — Проверяй свои настройки и данные!
    /settings — Настраивай меня под себя, дорогуша~
    Ну что, чем займёмся? 💕
    """,
        photo=types.FSInputFile("src/assets"),
    )
