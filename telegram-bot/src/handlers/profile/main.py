from aiogram import Router, types
from aiogram.filters import Command, or_f
from magic_filter import MagicFilter as F
from kb import profile_keyboard

router = Router(name="Profile")


@router.message(or_f(Command("profile"), F.text.contains("👤 Профиль")))
async def profile_handler(m: types.Message) -> None:
    user = ...  # todo реализовать AuthAdapter

    if user:
        return

    await m.reply_photo(
        photo=types.FSInputFile("src/assets/2.jpg"),
        reply_markup=profile_keyboard(is_authorized=False),
        caption=f"Ох, любимый~ ты всё ещё без авторизации? 😯\n"
        f"✨ Статус: Неавторизован, но я верю, ты всё настроишь! 😊\n"
        f"📺 Количество просмотренных аниме: Мне пока неизвестно, поделишься?\n"
        f"👤 Имя пользователя Shikimori: Эй, а ну быстро добавил! 😘\n"
        f"\nДавай, не заставляй меня скучать, любимый~ 🌸💕",
    )
