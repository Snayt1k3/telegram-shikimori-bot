from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from src.handlers.auth.kb import AuthCallBack, logout_keyboard, LogoutCallback
from src.adapters.auth import BaseAuthAdapter
from src.handlers.auth.state import AuthState

router = Router(name="auth")


@router.callback_query(AuthCallBack.filter(F.action == "login"))
async def login(
        call: types.CallbackQuery, auth_adapter: BaseAuthAdapter, state: FSMContext
) -> None:
    uri = await auth_adapter.get_uri()
    await call.message.answer(
        f"Хей-хей, Даааарлинг~ 💖\n"
        f"Я приготовила для тебя кое-что особенное! 🎀\n\n"
        f"Чтобы продолжить, переходи по этой ссылке: 🔗 {hlink('Ссылка', uri)}\n"
        f"После перехода тебе выдадут код – скопируй его и отправь мне сюда! 😘",
    )
    await state.set_state(AuthState.code)


@router.message(Command("login"))
async def login_handler(
        msg: types.Message, auth_adapter: BaseAuthAdapter, state: FSMContext
) -> None:
    uri = await auth_adapter.get_uri()
    await msg.answer(
        f"Хей-хей, Даааарлинг~ 💖\n"
        f"Я приготовила для тебя кое-что особенное! 🎀\n\n"
        f"Чтобы продолжить, переходи по этой ссылке: 🔗 {hlink("Ссылка", uri)}\n"
        f"После перехода тебе выдадут код – скопируй его и отправь мне сюда! 😘",
    )
    await state.set_state(AuthState.code)


@router.message(AuthState.code)
async def process_code(
        msg: types.Message, auth_adapter: BaseAuthAdapter, state: FSMContext
) -> None:
    await msg.answer(
        f"Ооо, Дааарлинг~ 💖\n\n"
        f"ижу, ты уже прислал код! 🎀 Дай-ка я быстренько его проверю… 🔍✨"
    )
    user = await auth_adapter.auth_user(msg.from_user.id, msg.text.strip())

    if user is None:
        await msg.answer(
            f"Эээй, Дааарлинг… 😢/n"
            f"Что-то тут не так! Код не подходит… 💔 Может, попробуешь ещё раз? 🤔🔄"
        )
    else:
        await msg.answer(
            f"Ураа, Дааарлинг~! 💖\n"
            f"Код проверен, и всё просто идеально! 🎀✨ Ты справился на ура! 🚀💋\n\n"
            f"Теперь давай шагнём дальше! Вызови команду /profile, и посмотрим, что у нас там~ 😏💕"
        )
    await state.clear()


@router.callback_query(AuthCallBack.filter(F.action == "logout"))
async def logout(call: types.CallbackQuery) -> None:
    await call.message.answer(
        f"Ооо, Дааарлинг… 🤨\n"
        f"Ты точно хочешь выйти? 💔 Мне будет скууучно без тебя… 😢\n"
        f"Если всё же передумаешь, просто скажи~ 💕",
        reply_markup=logout_keyboard(),
    )


@router.callback_query(LogoutCallback.filter(F.action == "Yes"))
async def logout_process(
        call: types.CallbackQuery, auth_adapter: BaseAuthAdapter
) -> None:
    await call.message.answer(
        "Эх, Дааарлинг… 😢\n"
        "Ты всё-таки выходишь… Ну ладно, я буду ждать твоего возвращения! 💕\n\n"
        "Не забывай про меня, окей? 😏✨"
    )
    await call.message.delete()
    # TODO: Добавить процесс выхода из система.


@router.callback_query(LogoutCallback.filter(F.action == "No"))
async def logout_cancel(call: types.CallbackQuery) -> None:
    await call.message.answer(
        f"Фух, Дааарлинг! 😍\n"
        f"Я уж подумала, что ты меня покидаешь… Но ты остался! 🎀💖\n\n"
        f"Продолжаем веселиться~ Что дальше? 😏💕"
    )
    await call.message.delete()
