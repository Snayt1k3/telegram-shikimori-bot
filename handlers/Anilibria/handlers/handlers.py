from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import anilibria_client
from database.repositories.anilibria import anilibria_repository
from handlers.Anilibria.utils.message import display_search_anime
from handlers.Anilibria.utils.states import AnimeFollow, start_get_torrent
from handlers.Anilibria.keyboards.inline import all_follows_kb


async def anime_follow_start(message: types.Message):
    """Standard start function for state"""
    await message.answer(
        "Напиши название тайтла, а я его поищу.\n" "Можете отменить - /cancel"
    )
    await AnimeFollow.anime_title.set()


async def anime_follow_end(message: types.Message, state: FSMContext):
    """get anime_title, and insert into db"""
    data = await anilibria_client.search_titles([message.text])

    # validation data
    if not data.list:
        await message.answer("Ничего не найдено.")
        return

    await anilibria_repository.insert_anilibria_list(
        message.chat.id, "anilibria_search", data.list
    )

    await display_search_anime(message)
    await state.finish()


async def all_follows(message: types.Message) -> None:
    """send list to user of his follows"""
    user_follows = await anilibria_repository.get_all_follows_by_user(message.chat.id)

    # check exists user follows
    if user_follows is None or not user_follows.follows:
        await message.answer(
            "Вы остались в неведении о выходе новых серий любимого аниме, "
            "так как забыли подписаться на обновления. 🤭"
        )
        return

    kb = await all_follows_kb(user_follows.follows)

    await message.bot.send_photo(
        message.chat.id,
        open("misc/img/pic2.png", "rb"),
        "Нажмите на интересующее вас аниме",
        reply_markup=kb,
    )


async def anime_get_torrent(message: types.Message):
    await start_get_torrent(message)


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(
        anime_follow_start, lambda msg: "Follow to Anime" in msg.text
    )
    dp.register_message_handler(all_follows, lambda msg: "Follows" in msg.text)
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
    dp.register_message_handler(anime_get_torrent, lambda msg: "torrent" in msg.text)
