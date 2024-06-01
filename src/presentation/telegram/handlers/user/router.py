from aiogram import Router
from aiogram.filters import Command

from src.presentation.telegram.common import SignOut, ShikimoriAuth
from .auth import sign_out, start_authorization, authorization_on_shiki, start_sign_out

usr_router = Router(name="user")


usr_router.callback_query.register(sign_out, SignOut.filter())

usr_router.message.register(start_sign_out, Command("signout"))
usr_router.message.register(authorization_on_shiki, ShikimoriAuth.code)
usr_router.message.register(start_authorization, Command("signin"))
