from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from Keyboard.reply import default_keyboard
from handlers.Anilibria.main import register_anilibria_handlers
from handlers.Shikimori.main import register_shiki_handlers
from handlers.admin.main import register_admin_handlers


async def send_commands(message: types.Message):

    await message.answer("ok", reply_markup=default_keyboard)


async def about_ru(message: types.message):
    await message.answer(
        "Обо мне\n"
        "Я бот позволяющий управлять вашим аккаунтом с shikimori,\n"
        "И еще я могу отправлять уведомление о выходе аниме в озвучки Anilibria \n\n"
        "Комманды:\n\n"
        "1. 🔍 Anime Search - Идет Поиск по отправленному вами названия тайтла, ищет на Shikimori\n\n"
        "2. 😁 My Profile - При первом вызове попросит скинуть ключ, а потом будет просто информация о "
        "вашем профиле\n\n"
        "3. 😐 Reset Profile - Отвязывает ваш профиль на Shikimori от бота\n\n"
        "4. 📽 My Watch List, 📃 My Planned List, ☑ My Completed List - "
        "Отправляет информация о ваших Списках с Shikimori \n\n"
        "5. ❤ My Follows - Отображение Аниме на которые вы подписались(Уведомления приходят Если Anilibria "
        "начала озвучивать новое аниме для них, или же онгоинг)\n\n"
        "6. 💌 Follow to Anime - Ищет по названию тайтла на Anilibria.tv, после нажатия на конкретное Аниме вам будет "
        "предложено - Найти его на Shikimori и отметить его, Подписаться на выход серий, Получить Torrent файл с "
        "озвучкой Anilibria\n\n"
        "7. ⬇ Get torrent - Ищет по названию тайтла на Anilibria.tv, после нажатия на конкретное Аниме вам будет "
        "Отправлен Торрент Файлы"
    )


async def about_en(message: types.Message):
    await message.answer(
        "About Me\n"
        "I am a bot that allows you to manage your shikimori account,\n"
        "And I can also send notifications about anime releases to Anilibria voiceover, this is only for Russians\n\n"
        "Commands:\n\n"
        "1. 🔍 Anime Search - Searching for the title you submitted, searching on Shikimori "
        "After clicking on a specific anime, the following actions will be available to you - "
        "add to Scheduled or Watched\n\n"
        "2. 😁 My Profile - At the first call, it will ask you to throw off the key, and then there will be just "
        "information about your profile\n\n"
        "3. 😐 Reset Profile - Unlinks your Shikimori profile from the bot\n\n"
        "4. 📽 My Watch List, 📃 My Planned List, ☑ My Completed List - "
        "Sends information about your Lists from Shikimori \n\n"
        "<b>Other commands, works only in Russian </b>",
        parse_mode='HTML'
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
    dp.register_message_handler(about_ru, commands=['aboutRu'])
    dp.register_message_handler(about_en, commands=['aboutEn'])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state='*')
    register_shiki_handlers(dp)
    register_anilibria_handlers(dp)
    register_admin_handlers(dp)
