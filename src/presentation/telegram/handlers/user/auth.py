from src.presentation.telegram.handlers.user.router import usr_router
from aiogram import types


@usr_router.message()  # TODO запуск Авторизации
async def start_authorization(msg: types.Message) -> None:
    """
    start authorization user on bot with his/her shikimori account
    """
    pass


@usr_router.message("Auth.code")  # TODO добавить состояние
async def authorization_on_shiki(msg: types.Message) -> None:
    """
    Getting auth code from msg and get access token, refresh token
    """
    pass


@usr_router.message()  # todo добавить команду для старта выхода из системы
async def start_sign_out(msg: types.Message) -> None:
    """
    Making sure what user really want to sign out
    """
    pass


@usr_router.callback_query()  # todo добавить строку callback
async def sign_out(msg: types.CallbackQuery) -> None:
    """
    delete user
    """
    pass
