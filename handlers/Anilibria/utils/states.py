from aiogram.dispatcher.filters.state import State, StatesGroup


class AnimeFollow(StatesGroup):
    anime_title = State()


class AnimeGetTorrent(StatesGroup):
    title = State()
