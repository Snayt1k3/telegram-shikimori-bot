from aiogram.dispatcher.filters.state import State, StatesGroup


class MarkAnime(StatesGroup):
    anime_title = State()
    score = State()
    status = State()


class AnimeSearch(StatesGroup):
    anime_str = State()


class UserNickname(StatesGroup):
    nick = State()


class UpdateScore(StatesGroup):
    score = State()


class UpdateScoreCompleted(StatesGroup):
    score = State()
