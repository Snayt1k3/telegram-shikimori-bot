from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from src.handlers.auth.kb import AuthCallBack, logout_keyboard, LogoutCallback
from src.adapters.http import BaseHttpAdapter
from src.handlers.auth.logic import get_uri, auth_user
from src.handlers.auth.state import AuthState

from magic_filter import MagicFilter as F

router = Router(name="auth")


@router.callback_query(AuthCallBack.filter(F.action == "login"))
async def login(
    call: types.CallbackQuery, http_adapter: BaseHttpAdapter, state: FSMContext
) -> None:
    uri = await get_uri(http_adapter)
    await call.message.answer(
        f"""
        Хей-хей, Даааарлинг~ 💖 \n
        Я приготовила для тебя кое-что особенное! 🎀\n\n
        
        Чтобы продолжить, переходи по этой ссылке: 🔗 {hlink("Ссылка", uri)}\n
        После перехода тебе выдадут код – скопируй его и отправь мне сюда! 😘"""
    )
    await state.set_state(AuthState.code)


@router.message(Command("login"))
async def login_handler(
    msg: types.Message, http_adapter: BaseHttpAdapter, state: FSMContext
) -> None:
    uri = await get_uri(http_adapter)
    await msg.answer(
        f"""
            Хей-хей, Даааарлинг~ 💖 \n
            Я приготовила для тебя кое-что особенное! 🎀\n\n

            Чтобы продолжить, переходи по этой ссылке: 🔗 {hlink("Ссылка", uri)}\n
            После перехода тебе выдадут код – скопируй его и отправь мне сюда! 😘"""
    )
    await state.set_state(AuthState.code)


@router.message(AuthState.code)
async def process_code(
    msg: types.Message, http_adapter: BaseHttpAdapter, state: FSMContext
) -> None:
    await msg.answer(
        """
        Ооо, Дааарлинг~ 💖\n\n

        Вижу, ты уже прислал код! 🎀 Дай-ка я быстренько его проверю… 🔍✨
        """
    )
    user = await auth_user(http_adapter, msg.from_user.id, msg.text.strip())

    if user is None:
        await msg.answer(
            """
            Эээй, Дааарлинг… 😢/n
            Что-то тут не так! Код не подходит… 💔 Может, попробуешь ещё раз? 🤔🔄
            """
        )
    else:
        await msg.answer(
            """
            Ураа, Дааарлинг~! 💖\n
            Код проверен, и всё просто идеально! 🎀✨ Ты справился на ура! 🚀💋\n\n
            Теперь давай шагнём дальше! Вызови команду /profile, и посмотрим, что у нас там~ 😏💕
            """
        )
    await state.clear()


@router.callback_query(AuthCallBack.filter(F.action == "logout"))
async def logout(call: types.CallbackQuery) -> None:

    await call.message.answer(
        text="""Ооо, Дааарлинг… 🤨\n
            Ты точно хочешь выйти? 💔 Мне будет скууучно без тебя… 😢\n
            Если всё же передумаешь, просто скажи~ 💕""",
        reply_markup=logout_keyboard(),
    )


@router.callback_query(LogoutCallback.filter(F.action == "Yes"))
async def logout_process(
    call: types.CallbackQuery, http_adapter: BaseHttpAdapter
) -> None:
    await call.message.answer(
        """
        Эх, Дааарлинг… 😢\n
        Ты всё-таки выходишь… Ну ладно, я буду ждать твоего возвращения! 💕\n\n
        Не забывай про меня, окей? 😏✨
    """
    )
    await call.message.delete()
    # TODO: Добавить процесс выхода из система.


@router.callback_query(LogoutCallback.filter(F.action == "No"))
async def logout_cancel(call: types.CallbackQuery) -> None:
    await call.message.answer(
        """
        Фух, Дааарлинг! 😍\n
        Я уж подумала, что ты меня покидаешь… Но ты остался! 🎀💖\n\n
        
        Продолжаем веселиться~ Что дальше? 😏💕
        """
    )
    await call.message.delete()
