from aiogram import Router, types
from aiogram.filters import Command, or_f
from magic_filter import MagicFilter as F

router = Router(name="Profile")


@router.message(or_f(Command("profile"), F.text.contains("👤 Профиль")))
@router.message()
async def profile_handler(m: types.Message) -> None:
    pass
