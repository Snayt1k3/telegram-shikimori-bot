from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot import anilibria_client
from database.repositories.anilibria import anilibria_repository
from Keyboard.anilibria import inline
from handlers.Anilibria.utils import message as msg_utils
from handlers.Anilibria.utils.states import AnimeFollow, AnimeGetTorrent


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

    await msg_utils.search_anime_msg(message)
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

    kb = await inline.all_follows_kb(user_follows.follows)

    await message.bot.send_photo(
        message.chat.id,
        open("misc/img/pic2.png", "rb"),
        "Нажмите на интересующее вас аниме",
        reply_markup=kb,
    )


async def anime_get_torrent(message: types.Message):
    await message.answer(
        f"Напиши названия тайтла, а я поищу его.\n" f"Можете отменить - /cancel."
    )
    await AnimeGetTorrent.title.set()


async def get_torrent_title(message: types.Message, state: FSMContext):
    await state.finish()
    animes = await anilibria_client.search_titles([message.text])

    kb = await inline.torrent_kb(animes.list)

    await message.reply_photo(
        open("misc/img/pic2.png", "rb"),
        reply_markup=kb,
        caption=f"Нажмите на интересующее вас аниме, чтобы получить торрент файл.",
    )


def register_anilibria_handlers(dp: Dispatcher):
    dp.register_message_handler(get_torrent_title, state=AnimeGetTorrent.title)
    dp.register_message_handler(anime_follow_end, state=AnimeFollow.anime_title)
    dp.register_message_handler(
        anime_follow_start, lambda msg: "Подписаться" in msg.text
    )
    dp.register_message_handler(all_follows, lambda msg: "Подписки" in msg.text)
    dp.register_message_handler(anime_get_torrent, lambda msg: "Торрент" in msg.text)
