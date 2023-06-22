from aiogram import Dispatcher, types


async def admin(message: types.Message):
    await message.answer('В разработке')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
