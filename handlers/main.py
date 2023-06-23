from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from Keyboard.reply import default_keyboard
from handlers.Anilibria.main import register_anilibria_handlers
from handlers.Shikimori.main import register_shiki_handlers
from handlers.admin.main import register_admin_handlers


async def send_commands(message: types.Message):
    await message.answer("ok", reply_markup=default_keyboard)


async def about(message: types.message):
    await message.answer(
        "Обо мне\n"
        "Я бот позволяющий управлять вашим аккаунтом с shikimori,\n"
        "И еще я могу отправлять уведомление о выходе аниме в озвучки Anilibria \n\n"
        "Комманды:\n\n"
        "1. 📌 Mark- Идет Поиск по отправленному вами названия тайтла, ищет на Shikimori\n\n"
        "2. 😁 My Profile - При первом вызове попросит скинуть ключ, а потом будет просто информация о "
        "вашем профиле\n\n"
        "3. 😐 Reset Profile - Отвязывает ваш профиль на Shikimori от бота\n\n"
        "4. 📄 Watch List, 📄 Planned List, 📄 Completed List - "
        "Отправляет информация о ваших Списках с Shikimori \n\n"
        "5. ❤️ Follows - Отображение Аниме на которые вы подписались(Уведомления приходят Если Anilibria "
        "начала озвучивать новое аниме, или же онгоинг)\n\n"
        "6. 💘 Follow to Anime - Ищет по названию тайтла на Anilibria.tv, после нажатия на конкретное Аниме вам будет "
        "предложено - Найти его на Shikimori и отметить его, Подписаться на выход серий, Получить Torrent файл с "
        "озвучкой Anilibria\n\n"
        "7. ⬇ Get torrent - Ищет по названию тайтла на Anilibria.tv, после нажатия на конкретное Аниме вам будет "
        "Отправлен Торрент Файл"
    )


async def cancel_handler(message: types.Message, state: FSMContext):
    """This handler allow cancel any states"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('ОК', reply_markup=default_keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_commands, commands=['commands'])
    dp.register_message_handler(about, commands=['about'])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    register_shiki_handlers(dp)
    register_anilibria_handlers(dp)
    register_admin_handlers(dp)
