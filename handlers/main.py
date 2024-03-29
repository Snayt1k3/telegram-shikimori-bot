from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from Keyboard.reply import default_keyboard
from handlers.Anilibria.main import register_anilibria_handlers
from handlers.Shikimori.main import register_shiki_handlers


async def send_commands(message: types.Message):
    await message.answer("OK", reply_markup=default_keyboard)


async def about(message: types.message):
    await message.reply_photo(
        photo=open("misc/img/shikimori_1.jpg", "rb"),
        caption="Обо мне\n"
        "Я бот позволяющий управлять вашим аккаунтом с Shikimori,\n"
        "И еще я могу отправлять уведомление о выходе аниме в озвучки Anilibria. \n\n"
        "Команды:\n\n"
        "1. 🔍 Поиск - Поиск аниме по названию на Shikimori.\n\n"
        "2. 😁 Profile - При первом вызове будет авторизация, а потом будет просто информация о "
        "вашем профиле.\n\n"
        "3. 😐 Unlink Profile - Отвязывает ваш профиль на Shikimori от бота.\n\n"
        "4. 📄 Смотрю, 📄 Планирую, 📄 Просмотрено - "
        "Отправляет информация о ваших списках с Shikimori. \n\n"
        "5. ❤️ Подписки - Отображение Аниме на которые вы подписались.\n\n"
        "6. 💘 Подписаться - Подписка на уведомления от Anilibria.\n\n"
        "7. ⬇ Торрент - Отправляет торрент файл.",
    )


async def cancel_handler(message: types.Message, state: FSMContext):
    """This handler allow cancel any states"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer("ОК", reply_markup=default_keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_commands, commands=["commands"])
    dp.register_message_handler(about, commands=["about"])
    dp.register_message_handler(
        cancel_handler, commands=["отмена", "cancel"], state="*"
    )
    register_shiki_handlers(dp)
    register_anilibria_handlers(dp)
