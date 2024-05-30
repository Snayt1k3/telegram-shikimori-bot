import logging

from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from src.adapters.clients import shiki_client
from src.adapters.database.common.db import get_session
from src.adapters.database.uow.uow import SqlAlchemyUnitOfWork
from src.application.dto import UserDTO
from src.application.usecases.user import (
    GetURIUseCase,
    SynchronizeUserRate,
    AddUserUseCase,
    DeleteUserUseCase
)
from src.presentation.telegram.common import Message
from src.presentation.telegram.common.keyboards import signout_kb, SignOut
from src.presentation.telegram.common.states import ShikimoriAuth
from src.presentation.telegram.handlers.user.router import usr_router

logger = logging.getLogger(__name__)

@usr_router.message(F.text, Command("signin"))
async def start_authorization(msg: types.Message, state: FSMContext) -> None:
    """
    start authorization user on bot with his/her shikimori account
    """
    await state.set_state(ShikimoriAuth.code)

    usecase = GetURIUseCase(shiki_client)
    uri = await usecase()

    await msg.answer(
        f"Чтобы продолжить нажмите сюда {hlink('Клик', uri)} и перешлите код сюда, который будет у вас на экране"
    )


@usr_router.message(ShikimoriAuth.code)
async def authorization_on_shiki(msg: types.Message, state: FSMContext) -> None:
    """
    Getting auth code from msg and get access token, refresh token and initialize user
    """
    try:
        await state.clear()
        uow = SqlAlchemyUnitOfWork(get_session)
        new_user = AddUserUseCase(shiki_client, uow)
        user: UserDTO = await new_user(msg.text, msg.from_user.id)

        sync = SynchronizeUserRate(shiki_client, uow)
        await msg.answer(
            "Началась Синхронизация вашего списка с шикимори в бота, вы можете продолжить пользоваться мной."
        )
        await sync(msg.from_user.id, user.creds.access)
        await msg.answer("Ваши списки загружены")

    except Exception as e:
        logger.error(f"Error occurred while initialize user - {e}")
        await msg.answer(
            "Что-то пошло не так, возможно вы отправили неверный код. Попробуйте еще раз /signin"
        )


@usr_router.message(
    F.text, Command("signout")
)
async def start_sign_out(msg: types.Message) -> None:
    """
    Making sure what user really want to sign out
    """
    text = Message.ensure_user_signout()
    markup = signout_kb()

    await msg.answer(text, reply_markup=markup)


@usr_router.callback_query(SignOut.filter())
async def sign_out(msg: types.CallbackQuery, data: SignOut) -> None:
    """
    delete user
    """

    if data.delete:
        uow = SqlAlchemyUnitOfWork(get_session)
        usecase = DeleteUserUseCase(uow)
        await usecase(msg.from_user.id)

    else:
        await msg.message.delete()
